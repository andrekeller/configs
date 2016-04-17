"""
confi.gs api mixins
"""
# 3rd-party
from tastypie.authentication import BasicAuthentication
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization


class AuthMixin:
    """
    Mixin to enable authentication & authorization on resources
    """
    authentication = MultiAuthentication(SessionAuthentication(),
                                         BasicAuthentication())
    authorization = DjangoAuthorization()
