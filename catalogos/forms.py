from django import forms

from catalogos.models import BusinessLine, Client, EscalationGroup, Priority, Product, TicketStatus


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "description", "maturity_level", "contact_email", "is_active"]


class BusinessLineForm(forms.ModelForm):
    class Meta:
        model = BusinessLine
        fields = ["name", "description", "is_active"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "business_line", "description", "is_active"]


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = TicketStatus
        fields = ["name", "description", "is_closed", "is_active"]


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ["name", "description", "severity", "sla_days", "is_active"]


class EscalationGroupForm(forms.ModelForm):
    class Meta:
        model = EscalationGroup
        fields = ["name", "description", "email", "is_active"]
