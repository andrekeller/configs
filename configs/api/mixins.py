from tastypie.authentication import BasicAuthentication
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization


class AuthMixin:
    authentication = MultiAuthentication(SessionAuthentication(),
                                         BasicAuthentication())
    authorization = DjangoAuthorization()
