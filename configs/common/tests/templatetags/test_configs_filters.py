"""
confi.gs common app tests for templatetags/configs_filters.py
"""
# stdlib
from urllib.parse import parse_qs
from urllib.parse import urlparse
# django
from django.core.urlresolvers import NoReverseMatch
from django.template import Context, Template
from django.test import TestCase


class FiltersTestCase(TestCase):

    def test_first_line(self):
        template_content = "{{ testvar|first_line }}"
        template = Template('{% load configs_filters %}' + template_content)

        context = Context({
            'testvar': "Some multiline text\nto showcase first_line filter",
        })
        self.assertEqual('Some multiline text', template.render(context))

        context = Context({'testvar': True, })
        with self.assertRaises(ValueError):
            template.render(context)

    def test_percentage(self):
        template_content = "{{ testvar|percentage }}"
        template = Template('{% load configs_filters %}' + template_content)

        context = Context({'testvar': 75.982, })
        self.assertEqual('76.0%', template.render(context))

        context = Context({'testvar': None, })
        self.assertEqual('0%', template.render(context))

        context = Context({'testvar': 0, })
        self.assertEqual('0%', template.render(context))

        context = Context({'testvar': "75.982", })
        with self.assertRaises(ValueError):
            template.render(context)

    def test_prefix_help_ipv4(self):
        template_content = "{{ testvar|prefix_help }}"
        template = Template('{% load configs_filters %}' + template_content)

        context = Context({'testvar': 0, })
        with self.assertRaises(ValueError):
            template.render(context)

        context = Context({'testvar': 32, })
        with self.assertRaises(ValueError):
            template.render(context)

        context = Context({'testvar': 29, })
        self.assertEqual(' (8 addresses)', template.render(context))

        context = Context({'testvar': 19, })
        self.assertEqual(' (8192 addresses)', template.render(context))

        context = Context({'testvar': "just a string", })
        with self.assertRaises(ValueError):
            template.render(context)

    def test_prefix_help_ipv6(self):
        template_content = "{{ testvar|prefix_help:6 }}"
        template = Template('{% load configs_filters %}' + template_content)

        context = Context({'testvar': 0, })
        with self.assertRaises(ValueError):
            template.render(context)

        context = Context({'testvar': 128, })
        with self.assertRaises(ValueError):
            template.render(context)

        context = Context({'testvar': 127, })
        self.assertEqual(' (2 addresses)', template.render(context))

        context = Context({'testvar': 126, })
        self.assertEqual(' (4 addresses)', template.render(context))

        context = Context({'testvar': 124, })
        self.assertEqual('', template.render(context))

        context = Context({'testvar': 64, })
        self.assertEqual(' network', template.render(context))

        context = Context({'testvar': 63, })
        self.assertEqual(' (2 /64 networks)', template.render(context))

        context = Context({'testvar': 49, })
        self.assertEqual(' (32768 /64 networks)', template.render(context))

        context = Context({'testvar': 48, })
        self.assertEqual(' (65536 /64 networks)', template.render(context))

        context = Context({'testvar': 47, })
        self.assertEqual(' (2 /48 networks)', template.render(context))

        context = Context({'testvar': 32, })
        self.assertEqual(' (65536 /48 networks)', template.render(context))

        context = Context({'testvar': "just a string", })
        with self.assertRaises(ValueError):
            template.render(context)

    def test_api_url(self):
        template_content = "{% api_url 'vrf' %}"
        template = Template('{% load configs_filters %}' + template_content)
        self.assertEqual(
            '/api/v1/vrf/',
            template.render(Context())
        )

        template_content = "{% api_url 'vlan' format='json' %}"
        template = Template('{% load configs_filters %}' + template_content)
        self.assertEqual(
            '/api/v1/vlan/?format=json',
            template.render(Context())
        )

        template_content = "{% api_url 'network' pk='1' format='yaml' %}"
        template = Template('{% load configs_filters %}' + template_content)
        rendered = template.render(Context())
        parsed_url = urlparse(rendered)
        format_arg = parse_qs(parsed_url[4])['format'][0]
        pk_arg = parse_qs(parsed_url[4])['pk'][0]
        self.assertEqual('/api/v1/network/', parsed_url[2])
        self.assertEqual('yaml', format_arg)
        self.assertEqual('1', pk_arg)

        template_content = "{% api_url 'unknown-endpoint' %}"
        template = Template('{% load configs_filters %}' + template_content)
        with self.assertRaises(NoReverseMatch):
            template.render(Context())
