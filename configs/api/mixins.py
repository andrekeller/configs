"""
configs api mixins.

bundles REST API mixins used by the other configs apps
"""

from rest_framework import authentication, permissions


class ApiDefaultsMixin:
    """
    Defines default attributes used by rest API viewsets
    """
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = None

