from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from catalogos.models import BusinessLine, Client, EscalationGroup, Priority, Product, TicketStatus


class Ticket(models.Model):
    internal_number = models.CharField("numero interno", max_length=40, unique=True)
    git_ticket = models.CharField("ticket GIT", max_length=80, blank=True)
    label = models.CharField("etiqueta", max_length=120)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="tickets")
    business_line = models.ForeignKey(BusinessLine, on_delete=models.PROTECT, related_name="tickets")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="tickets")
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT, related_name="tickets")
    escalated_to = models.ForeignKey(EscalationGroup, on_delete=models.PROTECT, related_name="tickets", null=True, blank=True)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name="tickets")
    description = models.TextField("descripcion")
    opened_at = models.DateField("fecha de apertura", default=timezone.localdate)
    resolved_at = models.DateField("fecha de resolucion", null=True, blank=True)
    reported_by = models.CharField("informado por", max_length=140)
    reporter_position = models.CharField("cargo", max_length=120, blank=True)
    reporter_email = models.EmailField("correo")
    reporter_phone = models.CharField("telefono", max_length=40, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assigned_tickets")
    observations = models.TextField("observaciones", blank=True)
    no_client_response = models.BooleanField("cerrado sin respuesta del cliente", default=False)
    negative_feedback = models.BooleanField("feedback negativo de producto", default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-opened_at", "-created_at"]
        permissions = [
            ("close_ticket", "Puede cerrar tickets"),
            ("export_ticket", "Puede exportar tickets"),
        ]

    def __str__(self):
        return f"{self.internal_number} - {self.label}"

    def get_absolute_url(self):
        return reverse("tickets:detail", kwargs={"pk": self.pk})

    @property
    def days_open(self):
        end_date = self.resolved_at or timezone.localdate()
        return max((end_date - self.opened_at).days, 0)

    @property
    def is_overdue(self):
        return not self.status.is_closed and self.days_open > self.priority.sla_days


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    body = models.TextField("comentario")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comentario {self.ticket.internal_number} por {self.author}"


class TicketFollowUp(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="followups")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField("accion", max_length=160)
    next_step = models.CharField("siguiente paso", max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Seguimiento {self.ticket.internal_number}: {self.action}"


class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    event = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "historial de ticket"
        verbose_name_plural = "historial de tickets"

    def __str__(self):
        return f"{self.ticket.internal_number} - {self.event}"
