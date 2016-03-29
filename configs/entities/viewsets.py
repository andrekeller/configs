from rest_framework import viewsets

from .serializers import EntitySerializer
from .models import Entity
from api.mixins import ApiDefaultsMixin


class EntityViewSet(ApiDefaultsMixin, viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
