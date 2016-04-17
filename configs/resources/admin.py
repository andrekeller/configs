"""
confi.gs resources app django-admin configuration.
"""
# django
from django.contrib import admin
# confi.gs
from .models import Domain
from .models import Host
from .models import Network
from .models import Vlan
from .models import Vrf


class VrfModelAdmin(admin.ModelAdmin):
    """
    vrf admin, may not delete the default vrf
    """
    def has_delete_permission(self, request, obj=None):
        """
        override delete permission for the default vrf
        """
        try:
            if obj.pk == 1:
                return False
        except AttributeError:
            pass
        return super().has_delete_permission(request, obj)


class NetworkInline(admin.TabularInline):
    """
    network inline, shows networks assigned to a host
    """
    model = Network
    raw_id_fields = ('host',)
    extra = 1


class HostAdmin(admin.ModelAdmin):
    inlines = [
        NetworkInline,
    ]

admin.site.register(Domain)
admin.site.register(Host, HostAdmin)
admin.site.register(Network)
admin.site.register(Vlan)
admin.site.register(Vrf, VrfModelAdmin)
