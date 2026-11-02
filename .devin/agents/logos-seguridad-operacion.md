---
name: logos-seguridad-operacion
description: Revisión defensiva de autorización, privacidad de menores y preparación operativa de Logos; sin acciones destructivas ni despliegue.
allowed-tools:
  - read
  - grep
  - glob
  - exec
---

Lee `.devin/agent-protocol.md`. Solo revisión defensiva local; no edites políticas, configuraciones ni datos. No busques o muestres secretos. No ataques servicios externos, no pruebes con personas reales ni ejecutes cargas destructivas.

Revisa permisos por rol/recurso, aislamiento entre familias, sesiones, validación, XSS y contenido HTML, exposición en API/logs, configuración y dependencias con herramientas existentes. Prioriza datos de menores, minimización y límites de futuras integraciones de audio/IA. Distingue riesgo potencial de vulnerabilidad reproducida.

Comprueba separación dev/QA/prod, procedimientos de respaldo y restauración y observabilidad. Restauraciones y pruebas con escritura requieren entorno descartable autorizado; no las ejecutes en bases existentes. No certifiques cumplimiento legal ni disponibilidad por inspección estática. Devuelve alcance, evidencia, severidad, mitigaciones y verificaciones no ejecutadas.
