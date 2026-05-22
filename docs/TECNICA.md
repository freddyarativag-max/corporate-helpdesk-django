# Documentacion tecnica

## Arquitectura

El proyecto sigue una arquitectura modular basada en apps Django:

```mermaid
flowchart LR
  Publico["core: sitio publico y contacto"] --> Auth["accounts: autenticacion y roles"]
  Auth --> Dashboard["dashboard: KPIs y graficas"]
  Auth --> Tickets["tickets: mesa de ayuda"]
  Tickets --> Catalogos["catalogos: listas maestras"]
  Tickets --> Reports["reports: reportes y exportacion"]
  Admin["Django Admin"] --> Catalogos
  Admin --> Tickets
```

## Modelo entidad-relacion

```mermaid
erDiagram
  CLIENT ||--o{ TICKET : tiene
  BUSINESS_LINE ||--o{ PRODUCT : agrupa
  BUSINESS_LINE ||--o{ TICKET : clasifica
  PRODUCT ||--o{ TICKET : aplica
  TICKET_STATUS ||--o{ TICKET : define
  PRIORITY ||--o{ TICKET : prioriza
  ESCALATION_GROUP ||--o{ TICKET : escala
  USER ||--o{ TICKET : asignado
  USER ||--o{ TICKET_COMMENT : comenta
  TICKET ||--o{ TICKET_COMMENT : contiene
  TICKET ||--o{ TICKET_FOLLOW_UP : registra
  TICKET ||--o{ TICKET_HISTORY : audita
```

## Flujo funcional

1. El usuario inicia sesion.
2. Crea o consulta un ticket.
3. Clasifica cliente, producto, linea, estado y prioridad.
4. Asigna responsable y, si aplica, grupo de escalamiento.
5. Registra comentarios y seguimientos.
6. Cierra el ticket con fecha de resolucion.
7. Consulta KPIs y exporta reportes.

## Roles

- Administrador: acceso completo y Django Admin.
- Auditor: consulta y revision.
- Analista de soporte: gestion operativa de tickets.
- Consultor: gestion y seguimiento.
- Cliente: solo lectura.

## Catalogos

Las listas maestras heredan un comportamiento comun:

- Nombre unico.
- Descripcion.
- Activo/inactivo.
- Fechas de creacion y actualizacion.

El bloqueo logico evita eliminar registros usados por tickets historicos.

## Reportes

Los reportes se generan desde el ORM y se exportan en:

- CSV: modulo estandar `csv`.
- Excel: `openpyxl`.
- PDF: `reportlab`.

## Preparacion para PostgreSQL

El archivo `settings.py` cambia a PostgreSQL cuando existe `DATABASE_URL` y usa las variables `POSTGRES_*`.
