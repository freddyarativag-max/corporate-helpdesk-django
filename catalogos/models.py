from django.db import models


class ActiveCatalogQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class CatalogBase(models.Model):
    name = models.CharField("nombre", max_length=140, unique=True)
    description = models.TextField("descripcion", blank=True)
    is_active = models.BooleanField("activo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveCatalogQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Client(CatalogBase):
    maturity_level = models.CharField("nivel de madurez", max_length=80, blank=True)
    contact_email = models.EmailField("correo de contacto", blank=True)

    class Meta(CatalogBase.Meta):
        verbose_name = "cliente"
        verbose_name_plural = "clientes"


class BusinessLine(CatalogBase):
    class Meta(CatalogBase.Meta):
        verbose_name = "linea de negocio"
        verbose_name_plural = "lineas de negocio"


class Product(CatalogBase):
    business_line = models.ForeignKey(BusinessLine, on_delete=models.PROTECT, related_name="products")

    class Meta(CatalogBase.Meta):
        verbose_name = "producto / app"
        verbose_name_plural = "productos / apps"


class TicketStatus(CatalogBase):
    is_closed = models.BooleanField("cierra ticket", default=False)

    class Meta(CatalogBase.Meta):
        verbose_name = "estado"
        verbose_name_plural = "estados"


class Priority(CatalogBase):
    severity = models.PositiveSmallIntegerField("severidad", default=2)
    sla_days = models.PositiveSmallIntegerField("SLA dias", default=15)

    class Meta(CatalogBase.Meta):
        verbose_name = "prioridad"
        verbose_name_plural = "prioridades"
        ordering = ["severity", "name"]


class EscalationGroup(CatalogBase):
    email = models.EmailField(blank=True)

    class Meta(CatalogBase.Meta):
        verbose_name = "grupo de escalamiento"
        verbose_name_plural = "grupos de escalamiento"
