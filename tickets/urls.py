from django.urls import path

from tickets import views

app_name = "tickets"

urlpatterns = [
    path("", views.TicketListView.as_view(), name="list"),
    path("crear/", views.TicketCreateView.as_view(), name="create"),
    path("exportar/csv/", views.export_csv, name="export_csv"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.TicketUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", views.TicketDeleteView.as_view(), name="delete"),
    path("<int:pk>/cerrar/", views.close_ticket, name="close"),
    path("<int:pk>/comentarios/", views.add_comment, name="comment"),
    path("<int:pk>/seguimientos/", views.add_followup, name="followup"),
]
