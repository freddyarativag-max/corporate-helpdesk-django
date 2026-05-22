import csv
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from tickets.models import Ticket


def report_rows(period):
    tickets = Ticket.objects.select_related("client", "status", "priority", "product")
    if period == "trimestral":
        tickets = tickets.order_by("-opened_at")[:90]
    elif period == "semestral":
        tickets = tickets.order_by("-opened_at")[:180]

    monthly = tickets.annotate(month=TruncMonth("opened_at")).values("month").annotate(total=Count("id")).order_by("month")
    return {
        "period": period,
        "total": tickets.count(),
        "monthly": monthly,
        "older_30": [t for t in tickets.filter(status__is_closed=False) if t.days_open > 30],
        "no_response": tickets.filter(no_client_response=True),
        "critical": tickets.filter(priority__name__icontains="crit"),
        "negative": tickets.filter(negative_feedback=True),
        "by_maturity": tickets.values("client__maturity_level").annotate(total=Count("id")).order_by("-total"),
    }


@login_required
def index(request):
    period = request.GET.get("period", "mensual")
    return render(request, "reports/index.html", report_rows(period))


@login_required
def export_csv(request):
    rows = report_rows(request.GET.get("period", "mensual"))
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="reporte_soporte.csv"'
    writer = csv.writer(response)
    writer.writerow(["Indicador", "Valor"])
    writer.writerow(["Total tickets", rows["total"]])
    writer.writerow(["Abiertos > 30 dias", len(rows["older_30"])])
    writer.writerow(["Cerrados sin respuesta", rows["no_response"].count()])
    writer.writerow(["Criticos", rows["critical"].count()])
    writer.writerow(["Feedback negativo", rows["negative"].count()])
    return response


@login_required
def export_excel(request):
    rows = report_rows(request.GET.get("period", "mensual"))
    wb = Workbook()
    ws = wb.active
    ws.title = "Indicadores"
    ws.append(["Indicador", "Valor"])
    ws.append(["Total tickets", rows["total"]])
    ws.append(["Abiertos > 30 dias", len(rows["older_30"])])
    ws.append(["Cerrados sin respuesta", rows["no_response"].count()])
    ws.append(["Criticos", rows["critical"].count()])
    ws.append(["Feedback negativo", rows["negative"].count()])
    output = BytesIO()
    wb.save(output)
    response = HttpResponse(output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="reporte_soporte.xlsx"'
    return response


@login_required
def export_pdf(request):
    rows = report_rows(request.GET.get("period", "mensual"))
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de soporte")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, 740, "Reporte de soporte tecnico")
    pdf.setFont("Helvetica", 11)
    y = 705
    for label, value in [
        ("Total tickets", rows["total"]),
        ("Abiertos mayores a 30 dias", len(rows["older_30"])),
        ("Cerrados sin respuesta", rows["no_response"].count()),
        ("Criticos", rows["critical"].count()),
        ("Feedback negativo", rows["negative"].count()),
    ]:
        pdf.drawString(72, y, f"{label}: {value}")
        y -= 24
    pdf.showPage()
    pdf.save()
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_soporte.pdf"'
    return response
