from django.contrib import admin

from catalogos.models import BusinessLine, Client, EscalationGroup, Priority, Product, TicketStatus


class CatalogAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Client)
class ClientAdmin(CatalogAdmin):
    list_display = ("name", "maturity_level", "contact_email", "is_active")


@admin.register(BusinessLine)
class BusinessLineAdmin(CatalogAdmin):
    pass


@admin.register(Product)
class ProductAdmin(CatalogAdmin):
    list_display = ("name", "business_line", "is_active")
    list_filter = ("business_line", "is_active")


@admin.register(TicketStatus)
class TicketStatusAdmin(CatalogAdmin):
    list_display = ("name", "is_closed", "is_active")


@admin.register(Priority)
class PriorityAdmin(CatalogAdmin):
    list_display = ("name", "severity", "sla_days", "is_active")


@admin.register(EscalationGroup)
class EscalationGroupAdmin(CatalogAdmin):
    list_display = ("name", "email", "is_active")
