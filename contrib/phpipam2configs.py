#!/usr/bin/env python3

"""Simple phpIPAM to confi.gs data migration script"""

# The MIT License (MIT)
#
# Copyright (c) 2016, André Keller, ak@0x2a.io
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ipaddress
import json
import logging
from argparse import ArgumentParser
from urllib.parse import urlencode

import requests


class JSONIpaddressEncoder(json.JSONEncoder):
    """JSON encoder with support for the ipaddress types"""

    # pylint: disable=method-hidden
    # see https://github.com/PyCQA/pylint/issues/414 and
    #     https://docs.python.org/3/library/json.html#json.JSONEncoder.default
    def default(self, obj):
        """
        Extend builtin JSONEncoder to support the ipaddress object types.

        This will return the compressed form of ipaddress.IPv4Network,
        ipaddress.IPv4Address, ipaddress.IPv6Address and ipaddress.IPv6Network

        Other object types are passed to the builtin JSON encoder.

        :param obj: object to serialize
        :return: serizalized object as string
        """
        if isinstance(obj, (ipaddress.IPv4Network,
                            ipaddress.IPv4Address,
                            ipaddress.IPv6Address,
                            ipaddress.IPv6Network)):
            return obj.compressed
        return json.JSONEncoder.default(self, obj)


class ConfigsApi:
    """Simple interface for the confi.gs API"""

    def __init__(self, url, user, password):
        """
        Initialize API and prepare authentication
        :param url: API URL
        :param user: API user
        :param password: API password
        """
        self.url = url
        self.auth = (user, password)

    def get(self, *resources, **parameters):
        """
        Request data from the API

        :param resources: API resource(s) to query
        :param parameters: Query parameters
        :return: dict if one result or list of dicts if multiple results
        """
        default_parameters = {
            'format': 'json',
        }
        default_parameters.update(parameters)
        resource_url = '%s/%s/?%s' % (
            self.url,
            '/'.join(list(resources)),
            urlencode(default_parameters)
        )
        req = requests.get(
            resource_url,
            auth=self.auth
        )
        req.raise_for_status()
        response = req.json()

        if response['meta']['total_count'] == 1:
            return response['objects'][0]
        return response['objects']

    def post(self, *resources, data):
        """
        Send data to the API

        :param resources: API resource to send data to
        :param data: data
        :return: Resource URI for newly created data
        """
        resource_url = '%s/%s/' % (self.url, '/'.join(list(resources)))
        req = requests.post(
            resource_url,
            data=json.dumps(data, cls=JSONIpaddressEncoder),
            auth=self.auth,
            headers={'Content-Type': 'application/json'},
        )
        req.raise_for_status()
        return req.headers['Location']


class PhpipamApi:
    """Simple interface to the phpIPAM v2 API"""

    def __init__(self, url, user, password):
        """
        Initialize and login to API
        :param url: API URL
        :param user: API user
        :param password: API password
        """
        self.url = url
        req = requests.post(
            '/'.join([self.url, 'user', '']),
            auth=(user, password)
        )
        req.raise_for_status()
        self.token = req.json().get('data', {}).get('token')

    def get(self, *args):
        """
        Request data from the API
        :param args: controllers
        :return: Queried data as dict
        """
        req = requests.get(
            '%s/%s/' % (self.url, '/'.join(list(args))),
            headers={'phpipam-token': self.token})
        return req.json()

    @property
    def sections(self):
        """
        Available sections

        :return: dict
        """
        return self.get('sections')['data']

    def get_subnets(self, section_id):
        """
        Get subnets for a specific section

        :param section_id: ID of section
        :return: list of dicts
        """
        return self.get('sections', section_id, 'subnets')['data']

    def get_vlan(self, vlan_id):
        """
        Get vlan by its phpIPAM id

        :param vlan_id: phpIPAM vlan id (not the vlan number!)
        :return: dict
        """
        return self.get('vlans', vlan_id)['data']

    def get_addresses(self, subnet_id):
        """
        Get addresses for subnet

        :param subnet_id: phpIPAM subnet id
        :return: dict
        """
        try:
            return self.get('subnets', subnet_id, 'addresses')['data']
        except KeyError:
            return {}


def parse_args():
    """
    Parse command line arguments

    :return: ArgumentParser namespace object
    """
    parser = ArgumentParser(
        prog='phpipam2configs',
        description='Simple phpIPAM to confi.gs migration script'
    )
    parser.add_argument(
        '--from-url', type=str, required=True,
        help='phpIPAM api url'
    )
    parser.add_argument(
        '--from-user', type=str, required=True,
        help='phpIPAM api user'
    )
    parser.add_argument(
        '--from-password', type=str, required=True,
        help='phpIPAM api password'
    )
    parser.add_argument(
        '--to-url', type=str, required=True,
        help='confi.gs api url'
    )
    parser.add_argument(
        '--to-user', type=str, required=True,
        help='confi.gs api user'
    )
    parser.add_argument(
        '--to-password', type=str, required=True,
        help='confi.gs api password'
    )
    parser.add_argument(
        '--debug', action='store_true', default=False,
        help='enable debug output'
    )
    return parser.parse_args()


def setup_logging(debug=False):
    """
    Setup logging

    :param debug: Whether to enable debug logging
    :return: logger object
    """
    if debug:
        main_loglevel = logging.DEBUG
        requests_loglevel = logging.DEBUG
    else:
        main_loglevel = logging.INFO
        requests_loglevel = logging.WARN

    logging.basicConfig(level=main_loglevel)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(level=requests_loglevel)
    return logging.getLogger('phpipam2configs')


def _configs_description(address):
    """
    will generate a confi.gs description from the phpIPAM equivalents.

    phpIPAM might store description in the description, hostname and/or the
    note field. this function combines those into a single field.

    :param address: dict of phpIPAM address object
    :return: description as str
    """
    description = []
    if address['description']:
        description.append(address['description'])

    if address['hostname']:
        if address['hostname'] != address['description']:
            description.append(address['hostname'])

    if address['note']:
        description.append(address['note'])

    return '\n'.join(description)


def phpipam2configs(phpipam, configs, logger):
    """
    Migrate phpIPAM content to confi.gs

    This function will walk through all the sections, subnets and addresses
    of phpIPAM and add the networks/hosts and vlans to confi.gs.

    :param phpipam PhpipamApi object
    :param configs ConfigsApi object
    :param logger logging.Logger object
    """

    # dict that will cache the confi.gs vlan uri (value) for a phpIPAM vlan
    # id (key).
    vlans = {}

    # phpIPAM has subnets divided in multiple logical sections
    for section in phpipam.sections:
        logger.debug('processing phpipam section "%s"', section['name'])

        # We will process each subnet from the current section
        for subnet in phpipam.get_subnets(section['id']):

            subnet_dict = {
                'use_reserved_addresses': False,
                'description': subnet['description'],
                # confi.gs does not store the netmask separate from the prefix
                'network': ipaddress.ip_network(
                    "%s/%s" % (subnet['subnet'], subnet['mask'])
                ),
            }
            logger.debug('processing phpipam subnet "%s"', subnet_dict['network'])

            # Process each address store for the current subnet
            for address in phpipam.get_addresses(subnet['id']):
                address_dict = {
                    'network': ipaddress.ip_address(address['ip']),
                }
                logger.debug('process phpipam address "%s"', address_dict['network'])

                # phpIPAM does not store whether or not reserved addresses are
                # allowed in a subnet. As confi.gs makes a hard distinction
                # we need to determine if there were such addresses within the
                # subnet in phpIPAM.
                if isinstance(subnet_dict['network'], ipaddress.IPv4Network):
                    if address_dict['network'] == subnet_dict['network'].broadcast_address:
                        subnet_dict['use_reserved_addresses'] = True
                if address_dict['network'] == subnet_dict['network'].network_address:
                    subnet_dict['use_reserved_addresses'] = True

                # phpIPAM has description stored in multiple fields, aggreagte
                # these into a single, line-separated string.
                address_dict['description'] = _configs_description(address)

                # Add the current address to confi.gs, unless its already there.
                # Only the network prefix is checked, so attributes wont be
                # synched in subsequent runs.
                try:
                    address_uri = configs.get(
                        'network',
                        network=address_dict['network'].compressed,
                    )['resource_uri']
                    logger.debug(
                        'network %s (phpipam address id: %s) already in confi.gs (%s)',
                        address_dict['network'],
                        address['id'],
                        address_uri
                    )
                except (requests.HTTPError, TypeError, KeyError):
                    address_uri = configs.post('network', data=address_dict)
                    logger.info(
                        'network %s (phpipam address id: %s) added to confi.gs (%s)',
                        address_dict['network'],
                        address['id'],
                        address_uri
                    )

            # if subnet belongs to a vlan, we fetch & sync vlan information
            # first so we can add the subnet with a single API call
            if subnet['vlanId'] != '0':

                # multiple subnets may be in the same vlan, so we store the
                # mapping phpIPAM vlan id <-> confi.gs vlan resource uri in
                # a local cache. This will ensure we issue only a single API
                # call for fetching each individual vlan
                try:
                    vlan_uri = vlans[subnet['vlanId']]
                    logger.debug(
                        'use cached info for vlan with phpipam id "%s"',
                        subnet['vlanId']
                    )
                except KeyError:
                    logger.debug(
                        'fetch vlan with id "%s" from phpipam',
                        subnet['vlanId']
                    )
                    phpipam_vlan = phpipam.get_vlan(subnet['vlanId'])

                    # Add the current vlan to confi.gs, unless its already there.
                    # Only the network prefix is checked, so attributes wont be
                    # synched in subsequent runs.
                    try:
                        vlan_uri = configs.get(
                            'vlan',
                            vlan_id=phpipam_vlan['number']
                        )['resource_uri']
                        logger.debug(
                            'vlan %s "%s" (phpipam id: %s) already in confi.gs (%s)',
                            phpipam_vlan['number'],
                            phpipam_vlan['name'],
                            subnet['vlanId'],
                            vlan_uri
                        )
                    except (requests.HTTPError, TypeError, KeyError):
                        vlan_uri = configs.post('vlan', data={
                            'vlan_id': phpipam_vlan['number'],
                            'vlan_name': phpipam_vlan['name']
                        })
                        logger.info(
                            'vlan %s "%s" (phpipam id: %s) added to confi.gs (%s)',
                            phpipam_vlan['number'],
                            phpipam_vlan['name'],
                            subnet['vlanId'],
                            vlan_uri
                        )

                # store the vlan request uri in our vlan mapping cache
                vlans[subnet['vlanId']] = vlan_uri
                # add the vlan_uri to the subnet data to be stored in
                # confi.gs
                subnet_dict['vlan'] = vlan_uri

            # Add the current subnet to confi.gs, unless its already there.
            # Only the network prefix is checked, so attributes wont be
            # synched in subsequent runs.
            try:
                network_uri = configs.get(
                    'network',
                    network=subnet_dict['network'].compressed,
                )['resource_uri']
                logger.debug(
                    'network %s (phpipam subnet id: %s) already in confi.gs (%s)',
                    subnet_dict['network'],
                    subnet['id'],
                    network_uri
                )
            except (requests.HTTPError, TypeError, KeyError):
                network_uri = configs.post('network', data=subnet_dict)
                logger.info(
                    'network %s (phpipam subnet id: %s) added to confi.gs (%s)',
                    subnet_dict['network'],
                    subnet['id'],
                    network_uri
                )


def main():
    """main function"""

    # parse commandline arguements
    args = parse_args()
    logger = setup_logging(args.debug)

    configs = ConfigsApi(
        url=args.to_url,
        user=args.to_user,
        password=args.to_password,
    )
    phpipam = PhpipamApi(
        url=args.from_url,
        user=args.from_user,
        password=args.from_password
    )

    # do the actual data migration
    phpipam2configs(phpipam, configs, logger=logger)


if __name__ == '__main__':
    main()
