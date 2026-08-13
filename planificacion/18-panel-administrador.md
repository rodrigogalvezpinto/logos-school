---
título: Panel de Administrador (dueño del proyecto)
estado: ✅ construido (2026-08-13) — login separado (`/admin/login`), Planes, Códigos de
  descuento, Cortesías y Métricas funcionando. 76/76 tests backend, 29/29 E2E.
última actualización: 2026-08-13
---

## Qué es

Un panel separado, solo para el usuario dueño del proyecto (y quien él autorice), para
gestionar el negocio sin tocar código ni pedirle a un desarrollador cada cambio menor.
Distinto del rol "Administrador/backoffice" de `01-roles-y-permisos.md` (que gestiona
contenido curricular y aprueba Profesores) — aquí el foco es **comercial**.

## Funciones

1. **Gestión de Planes**: crear, editar o desactivar planes (nombre, precio, nivel de
   acceso) sin necesitar un despliegue de código nuevo — los planes ya están modelados como
   una tabla (`Plan`, ver `11-especificacion-mvp-para-desarrollo.md`), este panel es la
   interfaz para editarla.
2. **Descuentos y ofertas**: crear códigos de descuento (porcentaje o monto fijo, con fecha
   de vencimiento opcional) aplicables al pagar un Plan.
3. **Cuentas de cortesía**: para el caso que el usuario mencionó explícitamente — poder
   darle a una familia específica acceso completo gratuito (por ejemplo, un año gratis, o
   indefinido) sin pasar por el flujo de pago. Se implementa como una **Suscripción especial**
   marcada `origen: "cortesia"` en vez de `origen: "pago"`, con la misma estructura de datos
   (mismo `Plan`, mismo modelo), solo que no requiere una transacción de pago asociada. El
   Administrador la asigna manualmente desde este panel, buscando al Alumno por su cuenta o
   RUT.
4. **Métricas básicas**: cuántos Apoderados/Alumnos registrados, cuántas Suscripciones
   activas por plan, ingresos del mes — vista simple, no un dashboard analítico complejo en
   el MVP.

## Modelo de datos adicional

```
CodigoDescuento
  id
  codigo                  (ej. "BIENVENIDA20")
  tipo                     ("porcentaje" | "monto_fijo")
  valor
  fecha_vencimiento        (nullable)
  usos_maximos              (nullable — sin límite si no se especifica)
  usos_actuales

Suscripcion  (actualiza la entidad ya definida en 11-especificacion-mvp-para-desarrollo.md)
  ...
  origen                   ("pago" | "cortesia")   ← campo nuevo
  codigo_descuento_id       (FK → CodigoDescuento, nullable)
```

## Cuándo se construye

**No es parte de la Fase 1.1** (que es autoestudio para el Alumno/Apoderado). Es la primera
pieza de una **Fase de Administración**, a construir en paralelo o justo después de la Fase
1.1, porque el usuario la necesita operativamente pronto (gestionar precios y dar cuentas de
cortesía es una necesidad real desde que haya usuarios reales, no algo que pueda esperar
meses). Se registra aquí para no perder el requisito, y se prioriza junto al dueño del
proyecto cuando la Fase 1.1 esté funcionando.
