from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    ADMIN = "admin"
    AUDITOR = "auditor"
    ANALYST = "analyst"
    CONSULTANT = "consultant"
    CLIENT = "client"

    ROLE_CHOICES = [
        (ADMIN, "Administrador"),
        (AUDITOR, "Auditor"),
        (ANALYST, "Analista de soporte"),
        (CONSULTANT, "Consultor"),
        (CLIENT, "Cliente"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)
    phone = models.CharField("telefono", max_length=40, blank=True)
    company = models.CharField("empresa", max_length=140, blank=True)

    class Meta:
        verbose_name = "perfil de usuario"
        verbose_name_plural = "perfiles de usuario"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"
