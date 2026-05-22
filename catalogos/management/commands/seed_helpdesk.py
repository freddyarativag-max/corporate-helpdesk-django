from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfile
from catalogos.models import BusinessLine, Client, EscalationGroup, Priority, Product, TicketStatus
from tickets.models import Ticket


class Command(BaseCommand):
    help = "Carga datos iniciales para probar la mesa de ayuda."

    def handle(self, *args, **options):
        User = get_user_model()
        admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True})
        admin.set_password("Admin12345!")
        admin.save()
        profile, _ = UserProfile.objects.get_or_create(user=admin)
        profile.role = UserProfile.ADMIN
        profile.save()

        analyst, _ = User.objects.get_or_create(username="analista", defaults={"email": "analista@example.com", "first_name": "Analista", "last_name": "Soporte"})
        analyst.set_password("Analista123!")
        analyst.save()
        analyst_profile, _ = UserProfile.objects.get_or_create(user=analyst)
        analyst_profile.role = UserProfile.ANALYST
        analyst_profile.save()

        client, _ = Client.objects.get_or_create(name="Cliente Corporativo Andino", defaults={"maturity_level": "Intermedio", "contact_email": "cliente@example.com"})
        line, _ = BusinessLine.objects.get_or_create(name="Analitica y gobierno")
        products = ["ACL Analytics", "Diligent HighBond", "Robots", "SAP Connector", "Resolver", "WRM", "AX", "Otros"]
        product_map = {name: Product.objects.get_or_create(name=name, business_line=line)[0] for name in products}
        statuses = {
            "Abierto": False,
            "En proceso": False,
            "Escalado": False,
            "Pendiente cliente": False,
            "Resuelto": True,
            "Cerrado": True,
        }
        status_map = {name: TicketStatus.objects.get_or_create(name=name, defaults={"is_closed": closed})[0] for name, closed in statuses.items()}
        priority_map = {
            "Baja": Priority.objects.get_or_create(name="Baja", defaults={"severity": 1, "sla_days": 30})[0],
            "Media": Priority.objects.get_or_create(name="Media", defaults={"severity": 2, "sla_days": 15})[0],
            "Alta": Priority.objects.get_or_create(name="Alta", defaults={"severity": 3, "sla_days": 7})[0],
            "Critica": Priority.objects.get_or_create(name="Critica", defaults={"severity": 4, "sla_days": 2})[0],
        }
        escalation, _ = EscalationGroup.objects.get_or_create(name="Soporte fabricante", defaults={"email": "vendor@example.com"})

        Ticket.objects.get_or_create(
            internal_number="HD-2026-0001",
            defaults={
                "git_ticket": "GIT-4512",
                "label": "Error en automatizacion mensual",
                "client": client,
                "business_line": line,
                "product": product_map["Robots"],
                "status": status_map["Escalado"],
                "escalated_to": escalation,
                "priority": priority_map["Alta"],
                "description": "El robot de conciliacion falla al procesar el lote mensual.",
                "opened_at": timezone.localdate(),
                "reported_by": "Laura Gomez",
                "reporter_position": "Audit Manager",
                "reporter_email": "laura@example.com",
                "reporter_phone": "+57 300 000 0000",
                "assigned_to": analyst,
                "created_by": admin,
                "observations": "Se escalo con trazas del job.",
            },
        )
        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados. Usuarios: admin/Admin12345! y analista/Analista123!"))
