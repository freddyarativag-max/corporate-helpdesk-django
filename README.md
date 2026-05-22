# Corporate Help Desk

Aplicacion web completa en Python y Django para gestionar solicitudes de soporte tecnico corporativo. Incluye autenticacion, roles, tickets, listas maestras, dashboard, reportes exportables y panel administrativo.

## Stack

- Python 3.13
- Django 6.0.4 (compatible con el requisito Django 5+)
- SQLite por defecto
- Preparado para PostgreSQL mediante variables de entorno
- Bootstrap 5, Bootstrap Icons y Chart.js
- OpenPyXL para Excel
- ReportLab para PDF

## Modulos

- `core`: pagina publica, contacto y presentacion corporativa.
- `accounts`: login, logout, recuperacion de contrasena y perfiles con roles.
- `catalogos`: clientes, lineas de negocio, productos, estados, prioridades y escalados.
- `tickets`: CRUD de tickets, cierre, busqueda, filtros, comentarios, seguimientos e historial.
- `dashboard`: KPIs y graficas operativas.
- `reports`: reportes mensuales, trimestrales y semestrales exportables a CSV, Excel y PDF.

## Instalacion local

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_helpdesk
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`.

Usuarios de prueba:

- Administrador: `admin` / `Admin12345!`
- Analista: `analista` / `Analista123!`

## Variables de entorno

Copia `.env.example` a `.env` y ajusta los valores.

Para SQLite no necesitas nada adicional. Para PostgreSQL:

```env
DATABASE_URL=postgres
POSTGRES_DB=helpdesk
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Funcionalidades principales

- Gestion completa de tickets: crear, editar, consultar, eliminar, cerrar, filtrar, buscar y exportar.
- Campos corporativos: numero interno, ticket GIT, cliente, linea, producto, estado, escalamiento, prioridad, fechas, reporter, asignado y observaciones.
- Estados sugeridos cargados por seed: abierto, en proceso, escalado, pendiente cliente, resuelto y cerrado.
- Prioridades: baja, media, alta y critica con SLA en dias.
- Comentarios, seguimientos e historial por ticket.
- Listas maestras editables desde UI y Django Admin.
- Bloqueo logico de catalogos obsoletos.
- Dashboard con tickets abiertos, cerrados, criticos, escalados, vencidos y tiempo promedio de resolucion.
- Reportes con comunicaciones por mes, tickets abiertos mayores a 30 dias, cierres sin respuesta, criticos, feedback negativo y madurez del cliente.
- Exportaciones: CSV, Excel y PDF.

## Seguridad

- Autenticacion Django.
- Hash seguro de contrasenas.
- Proteccion CSRF en formularios.
- Rutas privadas con `login_required`.
- Restricciones por rol para operaciones de escritura.
- Validaciones backend en formularios.
- Logging basico por consola.

## Infografia

La infografia generada con IA esta disponible en:

`static/img/helpdesk-infografia.png`

## Verificacion realizada

Se ejecutaron:

```powershell
python manage.py check
python manage.py makemigrations accounts catalogos tickets
python manage.py migrate
python manage.py seed_helpdesk
```

Tambien se verifico en navegador local:

- Pagina publica
- Login
- Dashboard
- Tickets
- Catalogos
- Reportes

## Despliegue

Para despliegue productivo:

- Define `DEBUG=False`.
- Configura `SECRET_KEY`.
- Configura `DJANGO_ALLOWED_HOSTS`.
- Usa PostgreSQL.
- Ejecuta `python manage.py collectstatic`.
- Configura un backend real de correo para recuperacion de contrasena.
