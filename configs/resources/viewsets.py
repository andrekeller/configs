"""
configs resources app REST-API viewsets
"""
from django.db import connection
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from api.mixins import ApiDefaultsMixin
from .serializers import NetworkSerializer, VlanSerializer, VrfSerializer
from .models import Network, Vlan, Vrf


class NetworkViewSet(ApiDefaultsMixin, viewsets.ModelViewSet):
    """
    network viewset
    """
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_backends = (filters.DjangoFilterBackend, )

    def _list(self, request, *args, **kwargs):
        # TODO: figure out a better way to make a rawqueryset pageable
        root_block_ids_query = Network.get_root_blocks().raw_query
        cursor = connection.cursor()
        try:
            cursor.execute(root_block_ids_query)
            queryset = Network.objects.filter(id__in=(x[0] for x in cursor))
        finally:
            cursor.close()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NetworkSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = NetworkSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)


class VlanViewSet(ApiDefaultsMixin, viewsets.ModelViewSet):
    """
    vlan viewset
    """
    queryset = Vlan.objects.all()
    serializer_class = VlanSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('vrf',)


class VrfViewSet(ApiDefaultsMixin, viewsets.ModelViewSet):
    """
    vrf viewset
    """
    queryset = Vrf.objects.all()
    serializer_class = VrfSerializer
