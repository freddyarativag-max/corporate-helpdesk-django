from django.urls import path

from catalogos import views

app_name = "catalogos"

urlpatterns = [
    path("<str:catalog>/", views.CatalogListView.as_view(), name="list"),
    path("<str:catalog>/crear/", views.CatalogCreateView.as_view(), name="create"),
    path("<str:catalog>/<int:pk>/editar/", views.CatalogUpdateView.as_view(), name="update"),
    path("<str:catalog>/<int:pk>/bloquear/", views.deactivate, name="deactivate"),
]
