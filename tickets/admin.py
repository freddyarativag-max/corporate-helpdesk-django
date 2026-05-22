from django.contrib import admin

from tickets.models import Ticket, TicketComment, TicketFollowUp, TicketHistory


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0


class TicketFollowUpInline(admin.TabularInline):
    model = TicketFollowUp
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("internal_number", "label", "client", "status", "priority", "assigned_to", "opened_at", "days_open")
    list_filter = ("status", "priority", "client", "business_line", "product")
    search_fields = ("internal_number", "git_ticket", "label", "description", "reporter_email")
    date_hierarchy = "opened_at"
    inlines = [TicketCommentInline, TicketFollowUpInline]


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ("ticket", "event", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("ticket__internal_number", "event")
