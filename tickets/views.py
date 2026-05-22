import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.permissions import RoleRequiredMixin, user_role
from catalogos.models import Client, Priority, TicketStatus
from tickets.forms import TicketCommentForm, TicketFollowUpForm, TicketForm
from tickets.models import Ticket, TicketHistory


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    paginate_by = 12
    template_name = "tickets/ticket_list.html"

    def get_queryset(self):
        queryset = Ticket.objects.select_related("client", "product", "status", "priority", "assigned_to")
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        client = self.request.GET.get("client")
        if query:
            queryset = queryset.filter(
                Q(internal_number__icontains=query) |
                Q(git_ticket__icontains=query) |
                Q(label__icontains=query) |
                Q(description__icontains=query) |
                Q(reporter_email__icontains=query)
            )
        if status:
            queryset = queryset.filter(status_id=status)
        if priority:
            queryset = queryset.filter(priority_id=priority)
        if client:
            queryset = queryset.filter(client_id=client)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "statuses": TicketStatus.objects.active(),
            "priorities": Priority.objects.active(),
            "clients": Client.objects.active(),
        })
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "tickets/ticket_detail.html"

    def get_queryset(self):
        return Ticket.objects.select_related("client", "product", "business_line", "status", "priority", "assigned_to", "escalated_to")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = TicketCommentForm()
        context["followup_form"] = TicketFollowUpForm()
        return context


class TicketCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        TicketHistory.objects.create(ticket=self.object, user=self.request.user, event="Ticket creado")
        messages.success(self.request, "Ticket creado correctamente.")
        return response


class TicketUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        TicketHistory.objects.create(ticket=self.object, user=self.request.user, event="Ticket actualizado")
        messages.success(self.request, "Ticket actualizado correctamente.")
        return response


class TicketDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Ticket
    template_name = "tickets/ticket_confirm_delete.html"
    success_url = reverse_lazy("tickets:list")

    def form_valid(self, form):
        messages.success(self.request, "Ticket eliminado correctamente.")
        return super().form_valid(form)


@login_required
def add_comment(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.ticket = ticket
        comment.author = request.user
        comment.save()
        TicketHistory.objects.create(ticket=ticket, user=request.user, event="Comentario agregado")
        messages.success(request, "Comentario agregado.")
    return redirect(ticket)


@login_required
def add_followup(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketFollowUpForm(request.POST)
    if form.is_valid():
        followup = form.save(commit=False)
        followup.ticket = ticket
        followup.author = request.user
        followup.save()
        TicketHistory.objects.create(ticket=ticket, user=request.user, event=f"Seguimiento: {followup.action}")
        messages.success(request, "Seguimiento registrado.")
    return redirect(ticket)


@login_required
@user_passes_test(lambda user: user_role(user) in {"admin", "analyst", "consultant"})
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    closed_status = TicketStatus.objects.filter(is_closed=True, is_active=True).first()
    if closed_status:
        ticket.status = closed_status
        ticket.resolved_at = ticket.resolved_at or timezone.localdate()
        ticket.save(update_fields=["status", "resolved_at", "updated_at"])
        TicketHistory.objects.create(ticket=ticket, user=request.user, event="Ticket cerrado")
        messages.success(request, "Ticket cerrado.")
    else:
        messages.error(request, "No existe un estado de cierre activo.")
    return redirect(ticket)


@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tickets.csv"'
    writer = csv.writer(response)
    writer.writerow(["Interno", "GIT", "Cliente", "Producto", "Estado", "Prioridad", "Apertura", "Resolucion", "Dias", "Asignado"])
    for ticket in Ticket.objects.select_related("client", "product", "status", "priority", "assigned_to"):
        writer.writerow([
            ticket.internal_number, ticket.git_ticket, ticket.client.name, ticket.product.name,
            ticket.status.name, ticket.priority.name, ticket.opened_at, ticket.resolved_at or "",
            ticket.days_open, ticket.assigned_to.get_full_name() or ticket.assigned_to.username,
        ])
    return response
