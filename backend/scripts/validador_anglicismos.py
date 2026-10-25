#!/usr/bin/env python3
"""
Validador de anglicismos en contenido educativo (texto en español).
Detecta palabras en inglés que no deben aparecer en material en español.
Uso: python validador_anglicismos.py [--fix] [ruta_archivo_o_directorio]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


# Lista de anglicismos detectados en la auditoría + comunes
ANGlicismos_PROHIBIDOS = {
    # Detectados en auditoría
    'population': 'población',
    'information': 'información',
    'dimensions': 'dimensiones',
    'welcome': 'bienvenida / vuelta',
    
    # Comunes en contenido educativo chileno
    'feedback': 'retroalimentación',
    'input': 'entrada / aporte',
    'output': 'salida / resultado',
    'workshop': 'taller',
    'online': 'en línea',
    'offline': 'fuera de línea',
    'login': 'inicio de sesión',
    'logout': 'cierre de sesión',
    'password': 'contraseña',
    'username': 'nombre de usuario',
    'email': 'correo electrónico',
    'link': 'enlace / vínculo',
    'click': 'clic',
    'download': 'descargar',
    'upload': 'subir / cargar',
    'streaming': 'transmisión en vivo',
    'webinar': 'seminario web',
    'backend': 'servidor / parte trasera',
    'frontend': 'interfaz / parte frontal',
    'database': 'base de datos',
    'server': 'servidor',
    'client': 'cliente',
    'api': 'API (mantener sigla)',
    'url': 'URL (mantener sigla)',
    'html': 'HTML (mantener sigla)',
    'css': 'CSS (mantener sigla)',
    'javascript': 'JavaScript (mantener nombre propio)',
    'python': 'Python (mantener nombre propio)',
    'sql': 'SQL (mantener sigla)',
    'json': 'JSON (mantener sigla)',
    'xml': 'XML (mantener sigla)',
    'csv': 'CSV (mantener sigla)',
    'pdf': 'PDF (mantener sigla)',
    'github': 'GitHub (mantener nombre propio)',
    'git': 'Git (mantener nombre propio)',
    'docker': 'Docker (mantener nombre propio)',
    'kubernetes': 'Kubernetes (mantener nombre propio)',
    'aws': 'AWS (mantener sigla)',
    'cloud': 'nube',
    'devops': 'DevOps (mantener nombre propio)',
    'agile': 'ágil',
    'scrum': 'Scrum (mantener nombre propio)',
    'sprint': 'iteración / sprint',
    'kanban': 'Kanban (mantener nombre propio)',
    'deploy': 'desplegar',
    'debug': 'depurar',
    'bug': 'error / fallo',
    'feature': 'funcionalidad / característica',
    'release': 'lanzamiento / versión',
    'commit': 'confirmar / commit',
    'push': 'enviar / push',
    'pull': 'traer / pull',
    'merge': 'fusionar / merge',
    'branch': 'rama',
    'fork': 'bifurcación / fork',
    'repo': 'repositorio',
    'issue': 'incidencia / problema',
    'ticket': 'ticket / incidencia',
    'staging': 'entorno de pruebas / preproducción',
    'production': 'producción',
    'localhost': 'localhost (mantener término técnico)',
    'endpoint': 'punto final / endpoint',
    'request': 'petición / solicitud',
    'response': 'respuesta',
    'header': 'cabecera',
    'payload': 'carga útil / cuerpo',
    'token': 'token (mantener término técnico)',
    'jwt': 'JWT (mantener sigla)',
    'oauth': 'OAuth (mantener sigla)',
    'ssl': 'SSL (mantener sigla)',
    'tls': 'TLS (mantener sigla)',
    'https': 'HTTPS (mantener sigla)',
    'http': 'HTTP (mantener sigla)',
    'dns': 'DNS (mantener sigla)',
    'ip': 'IP (mantener sigla)',
    'vpn': 'VPN (mantener sigla)',
    'ssh': 'SSH (mantener sigla)',
    'cli': 'CLI (mantener sigla)',
    'gui': 'GUI (mantener sigla)',
    'ui': 'UI (mantener sigla)',
    'ux': 'UX (mantener sigla)',
    'qa': 'QA (mantener sigla)',
    'ci': 'CI (mantener sigla)',
    'cd': 'CD (mantener sigla)',
    'pipeline': 'canalización / pipeline',
    'build': 'compilación / build',
    'test': 'prueba / test',
    'unit': 'unidad',
    'integration': 'integración',
    'e2e': 'E2E (mantener sigla)',
    'mock': 'simular / mock',
    'stub': 'stub / simulador',
    'spy': 'espía / spy',
    'coverage': 'cobertura',
    'benchmark': 'prueba de rendimiento / benchmark',
    'performance': 'rendimiento',
    'latency': 'latencia',
    'throughput': 'rendimiento / tasa de transferencia',
    'scalability': 'escalabilidad',
    'reliability': 'fiabilidad',
    'availability': 'disponibilidad',
    'monitoring': 'monitoreo',
    'logging': 'registro / logging',
    'alerting': 'alertas',
    'dashboard': 'panel / tablero',
    'metric': 'métrica',
    'kpi': 'KPI (mantener sigla)',
    'okr': 'OKR (mantener sigla)',
    'roadmap': 'hoja de ruta',
    'backlog': 'acumulación / backlog',
    'user story': 'historia de usuario',
    'acceptance criteria': 'criterios de aceptación',
    'definition of done': 'definición de terminado',
    'retrospective': 'retrospectiva',
    'daily': 'reunión diaria / daily',
    'standup': 'standup / reunión de pie',
    'planning': 'planificación',
    'review': 'revisión',
    'demo': 'demostración',
    'stakeholder': 'parte interesada',
    'product owner': 'dueño de producto',
    'scrum master': 'Scrum Master (mantener rol)',
    'developer': 'desarrollador',
    'designer': 'diseñador',
    'architect': 'arquitecto',
    'lead': 'líder / lead',
    'manager': 'gestor / manager',
    'director': 'director',
    'vp': 'VP (mantener sigla)',
    'cto': 'CTO (mantener sigla)',
    'ceo': 'CEO (mantener sigla)',
    'cfo': 'CFO (mantener sigla)',
    'hr': 'RRHH (recursos humanos)',
    'recruiting': 'reclutamiento',
    'onboarding': 'incorporación / inducción',
    'offboarding': 'desvinculación',
    'payroll': 'nómina / planilla',
    'benefits': 'beneficios',
    'perks': 'ventajas / beneficios',
    'equity': 'participación / acciones',
    'vesting': 'vesting / consolidación',
    'cliff': 'cliff / período inicial',
    'option pool': 'pool de opciones',
    'valuation': 'valoración',
    'fundraising': 'levantamiento de capital',
    'investor': 'inversor',
    'vc': 'VC (venture capital)',
    'angel': 'inversor ángel',
    'seed': 'semilla / ronda seed',
    'series a': 'serie A',
    'series b': 'serie B',
    'series c': 'serie C',
    'exit': 'salida / exit',
    'ipo': 'IPO (mantener sigla)',
    'm&a': 'M&A (fusiones y adquisiciones)',
    'due diligence': 'debida diligencia',
    'term sheet': 'hoja de términos',
    'cap table': 'tabla de capitalización',
    'dilution': 'dilución',
    'pro rata': 'pro rata',
    'liquidation preference': 'preferencia de liquidación',
    'anti-dilution': 'antidilución',
    'warrant': 'warrant / orden',
    'convertible note': 'pagaré convertible',
    'safe': 'SAFE (acuerdo simple para capital futuro)',
    'runway': 'pista / runway (meses de caja)',
    'burn rate': 'tasa de quema / burn rate',
    'cash flow': 'flujo de caja',
    'p&l': 'P&L (pérdidas y ganancias)',
    'balance sheet': 'balance general',
    'revenue': 'ingresos',
    'profit': 'ganancia / utilidad',
    'margin': 'margen',
    'ebitda': 'EBITDA (mantener sigla)',
    'arr': 'ARR (ingresos recurrentes anuales)',
    'mrr': 'MRR (ingresos recurrentes mensuales)',
    'churn': 'churn / tasa de cancelación',
    'ltv': 'LTV (valor de vida del cliente)',
    'cac': 'CAC (costo de adquisición de cliente)',
    'payback period': 'período de recuperación',
    'unit economics': 'economía unitaria',
    'cohort': 'cohorte',
    'retention': 'retención',
    'engagement': 'compromiso / engagement',
    'conversion': 'conversión',
    'funnel': 'embudo / funnel',
    'lead': 'cliente potencial / lead',
    'mql': 'MQL (lead calificado por marketing)',
    'sql': 'SQL (lead calificado por ventas)',
    'opportunity': 'oportunidad',
    'deal': 'trato / acuerdo',
    'pipeline': 'canal / pipeline',
    'forecast': 'pronóstico / forecast',
    'quota': 'cuota',
    'commission': 'comisión',
    'territory': 'territorio',
    'account': 'cuenta / cliente',
    'contact': 'contacto',
    'activity': 'actividad',
    'task': 'tarea',
    'event': 'evento',
    'campaign': 'campaña',
    'segment': 'segmento',
    'persona': 'persona / buyer persona',
    'journey': 'recorrido / journey',
    'touchpoint': 'punto de contacto',
    'attribution': 'atribución',
    'roi': 'ROI (mantener sigla)',
    'roas': 'ROAS (mantener sigla)',
    'cpm': 'CPM (costo por mil)',
    'cpc': 'CPC (costo por clic)',
    'cpa': 'CPA (costo por adquisición)',
    'ctr': 'CTR (tasa de clic)',
    'cvr': 'CVR (tasa de conversión)',
    'impression': 'impresión',
    'click': 'clic',
    'view': 'visualización',
    'reach': 'alcance',
    'frequency': 'frecuencia',
    'budget': 'presupuesto',
    'bid': 'puja',
    'ad': 'anuncio',
    'creative': 'creatividad',
    'copy': 'texto / copy',
    'headline': 'titular',
    'description': 'descripción',
    'call to action': 'llamada a la acción',
    'landing page': 'página de destino',
    'form': 'formulario',
    'field': 'campo',
    'validation': 'validación',
    'error': 'error',
    'success': 'éxito',
    'warning': 'advertencia',
    'info': 'información',
    'loading': 'cargando',
    'empty state': 'estado vacío',
    'placeholder': 'marcador de posición',
    'tooltip': 'información emergente / tooltip',
    'modal': 'modal / ventana emergente',
    'dropdown': 'desplegable',
    'checkbox': 'casilla de verificación',
    'radio button': 'botón de opción',
    'toggle': 'interruptor / toggle',
    'slider': 'deslizador',
    'datepicker': 'selector de fecha',
    'autocomplete': 'autocompletar',
    'search': 'buscar',
    'filter': 'filtrar',
    'sort': 'ordenar',
    'pagination': 'paginación',
    'infinite scroll': 'desplazamiento infinito',
    'lazy loading': 'carga perezosa',
    'skeleton': 'esqueleto / skeleton',
    'spinner': 'cargador / spinner',
    'progress bar': 'barra de progreso',
    'toast': 'notificación toast',
    'snackbar': 'snackbar',
    'banner': 'banner',
    'popup': 'ventana emergente',
    'dialog': 'diálogo',
    'sidebar': 'barra lateral',
    'navbar': 'barra de navegación',
    'header': 'encabezado',
    'footer': 'pie de página',
    'breadcrumb': 'migajas de pan',
    'tab': 'pestaña',
    'accordion': 'acordeón',
    'card': 'tarjeta',
    'list': 'lista',
    'grid': 'cuadrícula / grilla',
    'table': 'tabla',
    'chart': 'gráfico',
    'map': 'mapa',
    'calendar': 'calendario',
    'timeline': 'línea de tiempo',
    'kanban board': 'tablero Kanban',
    'gantt': 'Gantt (diagrama de Gantt)',
    'drag and drop': 'arrastrar y soltar',
    'resize': 'redimensionar',
    'zoom': 'zoom',
    'pan': 'desplazar',
    'rotate': 'rotar',
    'crop': 'recortar',
    'filter': 'filtro',
    'effect': 'efecto',
    'transition': 'transición',
    'animation': 'animación',
    'keyframe': 'fotograma clave',
    'easing': 'suavizado',
    'duration': 'duración',
    'delay': 'retraso',
    'iteration': 'iteración',
    'direction': 'dirección',
    'fill': 'relleno',
    'stroke': 'trazo',
    'opacity': 'opacidad',
    'visibility': 'visibilidad',
    'display': 'visualización',
    'position': 'posición',
    'absolute': 'absoluto',
    'relative': 'relativo',
    'fixed': 'fijo',
    'sticky': 'pegajoso / sticky',
    'float': 'flotar',
    'clear': 'limpiar / clear',
    'overflow': 'desbordamiento',
    'scroll': 'desplazamiento',
    'auto': 'automático',
    'hidden': 'oculto',
    'visible': 'visible',
    'collapse': 'colapsar',
    'expand': 'expandir',
    'show': 'mostrar',
    'hide': 'ocultar',
    'toggle': 'alternar',
    'open': 'abrir',
    'close': 'cerrar',
    'enable': 'habilitar',
    'disable': 'deshabilitar',
    'readonly': 'solo lectura',
    'required': 'requerido',
    'optional': 'opcional',
    'default': 'predeterminado',
    'value': 'valor',
    'label': 'etiqueta',
    'placeholder': 'marcador de posición',
    'help text': 'texto de ayuda',
    'error message': 'mensaje de error',
    'success message': 'mensaje de éxito',
    'warning message': 'mensaje de advertencia',
    'info message': 'mensaje informativo',
    'confirmation': 'confirmación',
    'cancel': 'cancelar',
    'save': 'guardar',
    'delete': 'eliminar',
    'edit': 'editar',
    'create': 'crear',
    'update': 'actualizar',
    'read': 'leer',
    'list': 'listar',
    'search': 'buscar',
    'filter': 'filtrar',
    'sort': 'ordenar',
    'export': 'exportar',
    'import': 'importar',
    'download': 'descargar',
    'upload': 'subir',
    'print': 'imprimir',
    'share': 'compartir',
    'copy': 'copiar',
    'paste': 'pegar',
    'cut': 'cortar',
    'undo': 'deshacer',
    'redo': 'rehacer',
    'select all': 'seleccionar todo',
    'deselect all': 'deseleccionar todo',
    'invert selection': 'invertir selección',
    'group': 'grupo',
    'ungroup': 'desagrupar',
    'lock': 'bloquear',
    'unlock': 'desbloquear',
    'duplicate': 'duplicar',
    'rename': 'renombrar',
    'move': 'mover',
    'archive': 'archivar',
    'restore': 'restaurar',
    'trash': 'papelera',
    'permanent delete': 'eliminar permanentemente',
    'settings': 'configuración',
    'preferences': 'preferencias',
    'profile': 'perfil',
    'account': 'cuenta',
    'password': 'contraseña',
    'security': 'seguridad',
    'privacy': 'privacidad',
    'notifications': 'notificaciones',
    'language': 'idioma',
    'timezone': 'zona horaria',
    'date format': 'formato de fecha',
    'time format': 'formato de hora',
    'currency': 'moneda',
    'theme': 'tema',
    'dark mode': 'modo oscuro',
    'light mode': 'modo claro',
    'system': 'sistema',
    'accessibility': 'accesibilidad',
    'screen reader': 'lector de pantalla',
    'keyboard navigation': 'navegación por teclado',
    'focus': 'foco',
    'contrast': 'contraste',
    'color blindness': 'daltonismo',
    'font size': 'tamaño de fuente',
    'line height': 'altura de línea',
    'letter spacing': 'espaciado entre letras',
    'word spacing': 'espaciado entre palabras',
    'text align': 'alineación de texto',
    'direction': 'dirección',
    'ltr': 'LTR (izquierda a derecha)',
    'rtl': 'RTL (derecha a izquierda)',
    'encoding': 'codificación',
    'utf-8': 'UTF-8 (mantener sigla)',
    'ascii': 'ASCII (mantener sigla)',
    'unicode': 'Unicode (mantener nombre propio)',
    'regex': 'regex / expresión regular',
    'json': 'JSON (mantener sigla)',
    'yaml': 'YAML (mantener sigla)',
    'toml': 'TOML (mantener sigla)',
    'xml': 'XML (mantener sigla)',
    'csv': 'CSV (mantener sigla)',
    'sql': 'SQL (mantener sigla)',
    'nosql': 'NoSQL (mantener sigla)',
    'orm': 'ORM (mantener sigla)',
    'migration': 'migración',
    'seed': 'datos semilla / seed',
    'factory': 'factoría / factory',
    'repository': 'repositorio',
    'service': 'servicio',
    'controller': 'controlador',
    'model': 'modelo',
    'view': 'vista',
    'template': 'plantilla',
    'layout': 'diseño / layout',
    'partial': 'parcial',
    'component': 'componente',
    'directive': 'directiva',
    'pipe': 'tubería / pipe',
    'guard': 'guarda / guard',
    'interceptor': 'interceptor',
    'resolver': 'resolvedor / resolver',
    'module': 'módulo',
    'provider': 'proveedor',
    'injectable': 'inyectable',
    'dependency injection': 'inyección de dependencias',
    'singleton': 'singleton / instancia única',
    'scoped': 'alcance / scoped',
    'transient': 'transitorio',
    'lifecycle': 'ciclo de vida',
    'hook': 'gancho / hook',
    'effect': 'efecto',
    'context': 'contexto',
    'ref': 'referencia / ref',
    'memo': 'memo / memoization',
    'callback': 'retrollamada / callback',
    'state': 'estado',
    'props': 'propiedades / props',
    'children': 'hijos / children',
    'render': 'renderizar',
    'mount': 'montar',
    'unmount': 'desmontar',
    'update': 'actualizar',
    'reconcile': 'conciliar / reconcile',
    'diff': 'diff / diferencia',
    'virtual dom': 'DOM virtual',
    'real dom': 'DOM real',
    'event': 'evento',
    'handler': 'manejador / handler',
    'listener': 'oyente / listener',
    'emit': 'emitir',
    'dispatch': 'despachar',
    'subscribe': 'suscribirse',
    'unsubscribe': 'desuscribirse',
    'observable': 'observable',
    'observer': 'observador',
    'subject': 'sujeto',
    'behavior subject': 'BehaviorSubject',
    'replay subject': 'ReplaySubject',
    'async subject': 'AsyncSubject',
    'operator': 'operador',
    'pipe': 'pipe / tubería',
    'map': 'map / mapear',
    'filter': 'filter / filtrar',
    'reduce': 'reduce / reducir',
    'merge': 'merge / fusionar',
    'concat': 'concat / concatenar',
    'zip': 'zip / combinar',
    'combineLatest': 'combineLatest',
    'forkJoin': 'forkJoin',
    'race': 'race / carrera',
    'catchError': 'catchError / atrapar error',
    'retry': 'retry / reintentar',
    'timeout': 'timeout / tiempo de espera',
    'debounce': 'debounce / antirrebote',
    'throttle': 'throttle / limitar tasa',
    'distinctUntilChanged': 'distinctUntilChanged',
    'scan': 'scan / escanear',
    'buffer': 'buffer / búfer',
    'window': 'window / ventana',
    'groupBy': 'groupBy / agrupar por',
    'partition': 'partition / particionar',
    'flatMap': 'flatMap / flatMap',
    'switchMap': 'switchMap / switchMap',
    'mergeMap': 'mergeMap / mergeMap',
    'concatMap': 'concatMap / concatMap',
    'exhaustMap': 'exhaustMap / exhaustMap',
    'expand': 'expand / expandir',
    'delay': 'delay / retrasar',
    'take': 'take / tomar',
    'skip': 'skip / saltar',
    'first': 'first / primero',
    'last': 'last / último',
    'single': 'single / único',
    'defaultIfEmpty': 'defaultIfEmpty',
    'startWith': 'startWith / empezar con',
    'endWith': 'endWith / terminar con',
    'repeat': 'repeat / repetir',
    'retryWhen': 'retryWhen / reintentar cuando',
    'catch': 'catch / atrapar',
    'finally': 'finally / finalmente',
    'using': 'using / usando',
    'defer': 'defer / diferir',
    'scheduler': 'scheduler / planificador',
    'async': 'async / asíncrono',
    'await': 'await / esperar',
    'promise': 'promise / promesa',
    'then': 'then / entonces',
    'catch': 'catch / atrapar',
    'finally': 'finally / finalmente',
    'async': 'async / asíncrono',
    'await': 'await / esperar',
    'generator': 'generador',
    'iterator': 'iterador',
    'yield': 'yield / producir',
    'next': 'next / siguiente',
    'return': 'return / retornar',
    'throw': 'throw / lanzar',
    'try': 'try / intentar',
    'catch': 'catch / atrapar',
    'finally': 'finally / finalmente',
    'async': 'async / asíncrono',
    'await': 'await / esperar',
}

# Palabras técnicas que SÍ pueden mantenerse en inglés (siglas, nombres propios)
EXCEPCIONES = {
    'api', 'url', 'html', 'css', 'javascript', 'python', 'sql', 'json', 'xml', 'csv', 'pdf',
    'github', 'git', 'docker', 'kubernetes', 'aws', 'devops', 'scrum', 'kanban',
    'jwt', 'oauth', 'ssl', 'tls', 'https', 'http', 'dns', 'ip', 'vpn', 'ssh', 'cli', 'gui', 'ui', 'ux',
    'qa', 'ci', 'cd', 'e2e', 'kpi', 'okr', 'vp', 'cto', 'ceo', 'cfo', 'ipo', 'm&a',
    'vc', 'arr', 'mrr', 'ltv', 'cac', 'ebitda', 'roi', 'roas', 'cpm', 'cpc', 'cpa', 'ctr', 'cvr',
    'utf-8', 'ascii', 'unicode', 'yaml', 'toml', 'nosql', 'orm', 'svg', 'png', 'jpg', 'jpeg', 'gif', 'webp',
    'http', 'https', 'ftp', 'smtp', 'imap', 'pop3', 'dns', 'dhcp', 'tcp', 'udp', 'icmp', 'arp',
    'cpu', 'gpu', 'ram', 'ssd', 'hdd', 'usb', 'hdmi', 'wifi', 'bluetooth', 'nfc', 'rfid', 'qr', 'qr code',
    'ai', 'ml', 'dl', 'nlp', 'cv', 'rl', 'gan', 'rnn', 'cnn', 'lstm', 'gru', 'bert', 'gpt', 't5',
    'api', 'rest', 'graphql', 'grpc', 'soap', 'rpc', 'websockets', 'webhook', 'oauth2', 'oidc', 'saml', 'ldap',
    'k8s', 'k3s', 'eks', 'gke', 'aks', 'helm', 'argocd', 'flux', 'istio', 'linkerd', 'consul', 'vault', 'nomad',
    'terraform', 'ansible', 'chef', 'puppet', 'saltstack', 'packer', 'vagrant', 'virtualbox', 'vmware', 'hyper-v',
    'aws', 'gcp', 'azure', 'digitalocean', 'linode', 'vultr', 'hetzner', 'scaleway', 'ovh',
    'ec2', 's3', 'lambda', 'dynamodb', 'rds', 'aurora', 'redshift', 'athena', 'glue', 'kinesis', 'sqs', 'sns',
    'cloudfront', 'route53', 'cloudwatch', 'cloudtrail', 'iam', 'cognito', 'secretsmanager', 'parameterstore',
    'vpc', 'subnet', 'securitygroup', 'nacl', 'igw', 'nat', 'elb', 'alb', 'nlb', 'clb',
    'ecs', 'ecr', 'fargate', 'ec2', 'autoscaling', 'elb', 'targetgroup', 'launchconfiguration', 'launchTemplate',
    'cloudformation', 'sam', 'cdk', 'serverless', 'apex', 'zappa', 'chalice',
    'jenkins', 'gitlab', 'github actions', 'bitbucket', 'circleci', 'travisci', 'drone', 'concourse', 'spinnaker',
    'prometheus', 'grafana', 'alertmanager', 'pushgateway', 'nodeexporter', 'blackboxexporter', 'cadvisor',
    'loki', 'promtail', 'fluentd', 'fluentbit', 'logstash', 'filebeat', 'metricbeat', 'packetbeat', 'heartbeat',
    'elasticsearch', 'kibana', 'logstash', 'beats', 'apm', 'uptime', 'synthetics', 'rum', 'synthetics',
    'jaeger', 'zipkin', 'opentelemetry', 'otel', 'trace', 'span', 'context', 'propagation', 'baggage',
    'sentry', 'rollbar', 'bugsnag', 'airbrake', 'honeybadger', 'raygun', 'newrelic', 'datadog', 'appdynamics',
    'pagerduty', 'opsgenie', 'victorops', 'xmatters', 'everbridge', 'alertops',
    'jira', 'confluence', 'bitbucket', 'bamboo', 'crowd', 'fisheye', 'crucible', 'statuspage', 'opsgenie',
    'trello', 'asana', 'monday', 'clickup', 'notion', 'airtable', 'smartsheet', 'wrike', 'basecamp', 'teamwork',
    'slack', 'teams', 'discord', 'zoom', 'meet', 'webex', 'gotomeeting', 'bluejeans', 'whereby', 'around',
    'gmail', 'outlook', 'yahoo', 'protonmail', 'fastmail', 'zoho', 'mailgun', 'sendgrid', 'postmark', 'sparkpost',
    'twilio', 'plivo', 'nexmo', 'vonage', 'bandwidth', 'telnyx', 'signalwire', 'messagebird', 'infobip',
    'stripe', 'paypal', 'square', 'adyen', 'braintree', 'checkout', '2checkout', 'authorize.net', 'worldpay',
    'globalpayments', 'firstdata', 'fiserv', 'fis', 'globalpayments', 'heartland', 'tsys', 'elavon', 'vantiv',
    'shopify', 'woocommerce', 'magento', 'bigcommerce', 'prestashop', 'opencart', 'shopware', 'sylius', 'spree',
    'wordpress', 'drupal', 'joomla', 'typo3', 'ghost', 'hugo', 'jekyll', 'gatsby', 'next', 'nuxt', 'gridsome',
    'react', 'vue', 'angular', 'svelte', 'solid', 'qwik', 'astro', 'remix', 'blitz', 'redwood', 'rails',
    'django', 'flask', 'fastapi', 'starlette', 'sanic', 'tornado', 'bottle', 'falcon', 'hug', 'molten',
    'express', 'koa', 'hapi', 'fastify', 'polka', 'sails', 'loopback', 'feathers', 'nest', 'adonis', 'strapi',
    'spring', 'springboot', 'micronaut', 'quarkus', 'helidon', 'vertx', 'ratpack', 'spark', 'dropwizard',
    'laravel', 'symfony', 'slim', 'lumen', 'codeigniter', 'cakephp', 'yii', 'phalcon', 'zend', 'fuelphp',
    'gin', 'echo', 'iris', 'beego', 'revel', 'buffalo', 'goa', 'gizmo', 'chi', 'mux', 'gorilla', 'httprouter',
    'actix', 'rocket', 'warp', 'tide', 'poem', 'salvo', 'thruster', 'hyper', 'tokio', 'async-std', 'smol',
    'django', 'flask', 'fastapi', 'starlette', 'sanic', 'tornado', 'bottle', 'falcon', 'hug', 'molten',
    'express', 'koa', 'hapi', 'fastify', 'polka', 'sails', 'loopback', 'feathers', 'nest', 'adonis', 'strapi',
    'spring', 'springboot', 'micronaut', 'quarkus', 'helidon', 'vertx', 'ratpack', 'spark', 'dropwizard',
    'laravel', 'symfony', 'slim', 'lumen', 'codeigniter', 'cakephp', 'yii', 'phalcon', 'zend', 'fuelphp',
    'gin', 'echo', 'iris', 'beego', 'revel', 'buffalo', 'goa', 'gizmo', 'chi', 'mux', 'gorilla', 'httprouter',
    'actix', 'rocket', 'warp', 'tide', 'poem', 'salvo', 'thruster', 'hyper', 'tokio', 'async-std', 'smol',
}


def cargar_diccionario_anglicismos() -> Dict[str, str]:
    """Retorna diccionario {anglicismo: sugerencia_español} filtrando excepciones."""
    resultado = {}
    for ing, esp in ANGlicismos_PROHIBIDOS.items():
        if ing.lower() not in EXCEPCIONES:
            resultado[ing.lower()] = esp
    return resultado


DICCIONARIO = cargar_diccionario_anglicismos()


def detectar_anglicismos(texto: str) -> List[Tuple[str, int, str]]:
    """
    Detecta anglicismos en un texto.
    Retorna lista de (palabra_encontrada, posicion, sugerencia).
    """
    hallazgos = []
    
    # Buscar palabras completas (bordes de palabra)
    for anglicismo, sugerencia in DICCIONARIO.items():
        # Patrón: palabra completa, case-insensitive
        patron = re.compile(r'\b' + re.escape(anglicismo) + r'\b', re.IGNORECASE)
        for match in patron.finditer(texto):
            hallazgos.append((match.group(), match.start(), sugerencia))
    
    # Ordenar por posición
    hallazgos.sort(key=lambda x: x[1])
    return hallazgos


def analizar_archivo(ruta: Path) -> Dict:
    """Analiza un archivo buscando anglicismos."""
    try:
        contenido = ruta.read_text(encoding='utf-8')
    except Exception as e:
        return {'archivo': str(ruta), 'error': str(e), 'hallazgos': []}
    
    hallazgos = detectar_anglicismos(contenido)
    
    # Agrupar por palabra única
    unicos = {}
    for palabra, pos, sug in hallazgos:
        key = palabra.lower()
        if key not in unicos:
            unicos[key] = {'palabra_original': palabra, 'sugerencia': sug, 'ocurrencias': 0, 'posiciones': []}
        unicos[key]['ocurrencias'] += 1
        unicos[key]['posiciones'].append(pos)
    
    return {
        'archivo': str(ruta),
        'total_hallazgos': len(hallazgos),
        'palabras_unicas': len(unicos),
        'detalle': unicos
    }


def corregir_archivo(ruta: Path, dry_run: bool = False) -> Tuple[int, str]:
    """Corrige anglicismos en un archivo (reemplaza por sugerencia en español)."""
    contenido = ruta.read_text(encoding='utf-8')
    original = contenido
    cambios = 0
    
    # Ordenar por longitud descendente para evitar reemplazos parciales
    anglicismos_ordenados = sorted(DICCIONARIO.keys(), key=len, reverse=True)
    
    for anglicismo in anglicismos_ordenados:
        sugerencia = DICCIONARIO[anglicismo]
        # Reemplazar case-insensitive preservando mayúscula inicial si la tenía
        def reemplazo(match):
            nonlocal cambios
            cambios += 1
            original_palabra = match.group()
            if original_palabra[0].isupper():
                return sugerencia.capitalize()
            return sugerencia
        
        patron = re.compile(r'\b' + re.escape(anglicismo) + r'\b', re.IGNORECASE)
        contenido = patron.sub(reemplazo, contenido)
    
    if not dry_run and contenido != original:
        ruta.write_text(contenido, encoding='utf-8')
    
    return cambios, contenido


def main():
    parser = argparse.ArgumentParser(description='Validador/Corrector de anglicismos en contenido español')
    parser.add_argument('ruta', nargs='?', default='contenido', help='Archivo o directorio a validar')
    parser.add_argument('--fix', action='store_true', help='Aplicar correcciones automáticas')
    parser.add_argument('--dry-run', action='store_true', help='Simular correcciones sin guardar')
    parser.add_argument('--ext', nargs='*', default=['.md', '.txt', '.py', '.html', '.ts', '.js', '.vue', '.svelte'],
                        help='Extensiones de archivo a procesar')
    args = parser.parse_args()
    
    ruta = Path(args.ruta)
    
    if not ruta.exists():
        print(f"[ERROR] Ruta no existe: {ruta}")
        sys.exit(1)
    
    extensiones = set(args.ext)
    
    if ruta.is_file():
        if ruta.suffix not in extensiones:
            print(f"[WARN] Extensión {ruta.suffix} no está en lista permitida")
        resultado = analizar_archivo(ruta)
        print(f"\n[FILE] {resultado['archivo']}")
        print(f"   Total hallazgos: {resultado['total_hallazgos']}")
        print(f"   Palabras únicas: {resultado['palabras_unicas']}")
        for palabra, info in resultado['detalle'].items():
            print(f"   - '{info['palabra_original']}' → '{info['sugerencia']}' ({info['ocurrencias']} veces)")
        
        if args.fix or args.dry_run:
            cambios, _ = corregir_archivo(ruta, dry_run=args.dry_run)
            accion = "Simulados" if args.dry_run else "Aplicados"
            print(f"   {accion} {cambios} correcciones")
    else:
        archivos = []
        for ext in extensiones:
            archivos.extend(ruta.rglob(f'*{ext}'))
        
        print(f"[SCAN] Escaneando {len(archivos)} archivos en {ruta}...")
        
        total_archivos_con_hallazgos = 0
        total_hallazgos = 0
        total_cambios = 0
        
        for archivo in sorted(archivos):
            resultado = analizar_archivo(archivo)
            if resultado.get('total_hallazgos', 0) > 0:
                total_archivos_con_hallazgos += 1
                total_hallazgos += resultado['total_hallazgos']
                print(f"\n[FILE] {resultado['archivo']}")
                print(f"   {resultado['total_hallazgos']} hallazgos ({resultado['palabras_unicas']} unicos)")
                for palabra, info in resultado['detalle'].items():
                    print(f"   - '{info['palabra_original']}' -> '{info['sugerencia']}' ({info['ocurrencias']}x)")
                
                if args.fix or args.dry_run:
                    cambios, _ = corregir_archivo(archivo, dry_run=args.dry_run)
                    total_cambios += cambios
                    accion = "Simulados" if args.dry_run else "Aplicados"
                    print(f"   {accion} {cambios} correcciones")
        
        print(f"\n[RESUMEN]")
        print(f"   Archivos escaneados: {len(archivos)}")
        print(f"   Archivos con anglicismos: {total_archivos_con_hallazgos}")
        print(f"   Total hallazgos: {total_hallazgos}")
        if args.fix or args.dry_run:
            accion = "Simuladas" if args.dry_run else "Aplicadas"
            print(f"   Correcciones {accion}: {total_cambios}")


if __name__ == '__main__':
    main()