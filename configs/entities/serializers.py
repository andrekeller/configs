from rest_framework import serializers
from rest_framework.reverse import reverse
from entities.models import Entity


class EntitySerializer(serializers.HyperlinkedModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = (
            'id',
            'name',
            'notes',
            'links',
        )

    def get_links(self, obj):

        request = self.context['request']
        return {
            'self': reverse('entity-detail',
                            kwargs={'pk': obj.pk}, request=request),
        }
