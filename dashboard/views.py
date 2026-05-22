from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from tickets.models import Ticket


@login_required
def home(request):
    tickets = Ticket.objects.select_related("client", "priority", "status", "assigned_to")
    start = request.GET.get("start")
    end = request.GET.get("end")
    if start:
        tickets = tickets.filter(opened_at__gte=start)
    if end:
        tickets = tickets.filter(opened_at__lte=end)

    open_qs = tickets.filter(status__is_closed=False)
    closed_qs = tickets.filter(status__is_closed=True)
    overdue = [ticket for ticket in open_qs if ticket.is_overdue]
    avg_resolution = closed_qs.exclude(resolved_at__isnull=True).annotate(
        resolution_days=F("resolved_at") - F("opened_at")
    ).aggregate(avg=Avg("resolution_days"))["avg"]

    context = {
        "tickets_open": open_qs.count(),
        "tickets_closed": closed_qs.count(),
        "tickets_critical": tickets.filter(priority__name__icontains="crit").count(),
        "tickets_escalated": tickets.exclude(escalated_to__isnull=True).count(),
        "tickets_overdue": len(overdue),
        "avg_resolution": avg_resolution.days if avg_resolution else 0,
        "by_client": list(tickets.values("client__name").annotate(total=Count("id")).order_by("-total")[:8]),
        "by_analyst": list(tickets.values("assigned_to__username").annotate(total=Count("id")).order_by("-total")[:8]),
        "recent_tickets": tickets[:8],
        "today": timezone.localdate(),
    }
    return render(request, "dashboard/home.html", context)
