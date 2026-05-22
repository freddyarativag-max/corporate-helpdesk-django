from django import forms

from tickets.models import Ticket, TicketComment, TicketFollowUp


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "internal_number", "git_ticket", "label", "client", "business_line", "product",
            "status", "escalated_to", "priority", "description", "opened_at", "resolved_at",
            "reported_by", "reporter_position", "reporter_email", "reporter_phone",
            "assigned_to", "observations", "no_client_response", "negative_feedback",
        ]
        widgets = {
            "opened_at": forms.DateInput(attrs={"type": "date"}),
            "resolved_at": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "observations": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        opened_at = cleaned.get("opened_at")
        resolved_at = cleaned.get("resolved_at")
        if opened_at and resolved_at and resolved_at < opened_at:
            self.add_error("resolved_at", "La fecha de resolucion no puede ser anterior a la apertura.")
        return cleaned


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Agregar comentario..."})}


class TicketFollowUpForm(forms.ModelForm):
    class Meta:
        model = TicketFollowUp
        fields = ["action", "next_step"]
