"""
configs resource app django-admin configuration.
"""
from django.contrib import admin
from resources.models import Domain, Host, Network, Vlan, Vrf


class VrfModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        try:
            if obj.pk == 1:
                return False
        except AttributeError:
            pass
        return super().has_delete_permission(request, obj)


class NetworkInline(admin.TabularInline):
    model = Network
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
