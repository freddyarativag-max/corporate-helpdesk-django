from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from accounts.permissions import RoleRequiredMixin, user_role
from catalogos.forms import BusinessLineForm, ClientForm, EscalationGroupForm, PriorityForm, ProductForm, TicketStatusForm
from catalogos.models import BusinessLine, Client, EscalationGroup, Priority, Product, TicketStatus


CATALOGS = {
    "clientes": (Client, ClientForm, "Clientes"),
    "lineas": (BusinessLine, BusinessLineForm, "Lineas de negocio"),
    "productos": (Product, ProductForm, "Productos / APP"),
    "estados": (TicketStatus, TicketStatusForm, "Estados"),
    "prioridades": (Priority, PriorityForm, "Prioridades"),
    "escalados": (EscalationGroup, EscalationGroupForm, "Escalados"),
}


class CatalogListView(LoginRequiredMixin, ListView):
    template_name = "catalogos/catalog_list.html"
    paginate_by = 15

    def dispatch(self, request, *args, **kwargs):
        self.model, self.form_class, self.title = CATALOGS[kwargs["catalog"]]
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"catalog": self.kwargs["catalog"], "title": self.title})
        return context


class CatalogCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    template_name = "catalogos/catalog_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.model, self.form_class, self.title = CATALOGS[kwargs["catalog"]]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("catalogos:list", kwargs={"catalog": self.kwargs["catalog"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title, "catalog": self.kwargs["catalog"]})
        return context


class CatalogUpdateView(CatalogCreateView, UpdateView):
    pass


@login_required
@user_passes_test(lambda user: user_role(user) in {"admin", "analyst", "consultant"})
def deactivate(request, catalog, pk):
    model, _, title = CATALOGS[catalog]
    obj = get_object_or_404(model, pk=pk)
    obj.is_active = False
    obj.save(update_fields=["is_active", "updated_at"])
    messages.success(request, f"{title}: registro bloqueado sin eliminacion fisica.")
    return redirect("catalogos:list", catalog=catalog)
