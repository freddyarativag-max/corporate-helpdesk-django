from django.contrib import messages
from django.shortcuts import redirect, render

from core.forms import ContactForm
from tickets.models import Ticket


def home(request):
    context = {
        "open_tickets": Ticket.objects.filter(status__is_closed=False).count(),
        "closed_tickets": Ticket.objects.filter(status__is_closed=True).count(),
        "clients_count": Ticket.objects.values("client").distinct().count(),
        "critical_count": Ticket.objects.filter(priority__name__icontains="crit").count(),
    }
    return render(request, "core/home.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "Gracias. Tu mensaje fue registrado para seguimiento comercial.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form})
