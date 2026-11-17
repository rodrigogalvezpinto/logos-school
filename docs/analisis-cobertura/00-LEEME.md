# Análisis de cobertura del temario oficial (iniciado 2026-11-17)

Pedido del dueño: identificar **dónde el material no cumple** con lo que el Mineduc exige estudiar para el examen libre,
en cada curso y asignatura. **Solo análisis; las correcciones esperan su decisión.**

Método:
1. `scripts/analisis/cobertura_temario.py` cruza los 410 OA y 1.528 indicadores de `Temarios/analisis/` con la base
   (explicación de la guía y preguntas por OA). Resultado: los 410 OA existen en el material.
2. `scripts/analisis/volcar_curso.py "<curso>" <json>` vuelca, por curso, cada OA con sus indicadores y el texto de la guía.
3. Lectura humana indicador por indicador; el resultado de cada curso queda en `NN-curso.md` de esta carpeta.

Clasificación de brechas: **Falta** (el indicador no se enseña), **Falta parcial**, **Débil** (se menciona sin ejemplo o
sin la profundidad que pide el indicador), **Visual** (mapa o imagen pendiente), **Poca práctica** (pocas preguntas
fuera de la guía).

Estado: **análisis terminado (2026-11-17), 12/12 cursos revisados.** Archivos: `01-basico.md` … `08-basico.md`,
`09-1-medio.md`, `10-2-medio.md`, `11-3-medio.md`, `12-4-medio.md`.

## Resumen consolidado

**Conclusión general:** los **410 OA del temario oficial están todos en el material**, cada uno con explicación, ejemplos
resueltos y preguntas. **No hay ningún OA ausente.** Las brechas (93 en total) son de profundidad dentro de un OA:
un indicador sin ejemplo, una figura o mapa que no se muestra, o poca práctica fuera de la guía.

| Curso | OA | Brechas | Lo más relevante |
|---|---|---|---|
| 1.° básico | 27/27 | 5 | Crear un problema (Mat OA 9); agrupar seres vivos; mapa de Chile; 2 `[Imagen]` |
| 2.° básico | 33/33 | 7 | Pirámide y cilindro faltan (Mat OA 16); crear patrón; mapas; 5 `[Imagen]` |
| 3.° básico | 29/29 | 6 | Tablas sin representación pictórica; mapa del mundo; 1 `[Imagen]` |
| 4.° básico | 32/32 | 5 | Números en palabras; algoritmo vertical; fracciones sin figura; mapa de América |
| 5.° básico | 43/43 | 11 | Áreas irregulares (Mat OA 22); Inglés: vocabulario temático y guías breves; mapa de zonas |
| 6.° básico | 44/44 | 6 | Inglés: vocabulario de ciudad/ocupaciones/transporte; balanza pictórica; mapas |
| 7.° básico | 39/39 | 6 | Inglés: vocabulario temático; problemas algebraicos; leer gráficos |
| 8.° básico | 40/40 | 11 | **Ecuaciones/inecuaciones: 4 de 7 formas sin ejemplo y ninguna inecuación**; Inglés vocabulario |
| 1.° medio | 40/40 | 13 | Euclides sin preguntas; comparación de planetas; Inglés vocabulario; mapas |
| 2.° medio | 39/39 | 17 | **Función cuadrática sin gráfico y sin problemas con ecuación cuadrática**; populismos (Brasil, México) |
| 3.° medio | 24/24 | 4 | Circunferencia sin figura; práctica de Matemática |
| 4.° medio | 20/20 | 2 | Práctica de créditos y modelos trigonométricos |

### Patrones que se repiten (corregirlos por patrón es más rápido que curso por curso)

1. **Inglés, vocabulario temático (5.° básico a 2.° medio, 6 cursos).** Cada temario trae listas de vocabulario por tema
   (comida, ropa, ciudad, ocupaciones, TIC, viajes, globalización, tecnología, etc.). Las guías enseñan bien la gramática,
   pero esas listas casi no aparecen, y el examen de Inglés las usa. Es la brecha más extendida.
2. **Matemática, procedimientos con un solo ejemplo o ninguno.** Los casos más serios son 8.° básico (ecuaciones e
   inecuaciones) y 2.° medio (función cuadrática). También: «crear un problema o patrón» (1.°–3.° básico), números en
   palabras (4.°), áreas irregulares (5.°), potencia de potencia, Pitágoras en 3D (8.°).
3. **Figuras que se describen en palabras en vez de mostrarse.** En Matemática: parábola, circunferencia, homotecia,
   función inversa, balanza, fracciones. En Historia: mapas en 1.° básico a 2.° medio. Ya existen los marcadores
   `::mapa::america|sudamerica|chile|mesoamerica|mediterraneo::` y no se usan en varios OA. Faltan un mapa del mundo
   (3.° básico, Guerra Fría) y uno de regiones de Chile (6.° básico).
4. **Poca práctica de Matemática fuera de la guía.** En 1.° a 6.° básico varios OA tienen solo 1 pregunta en pruebas de
   unidad. En media faltan problemas contextualizados (trigonometría, combinatoria, logaritmos, Euclides).
5. **Imágenes pendientes `[Imagen: …]`:** 8 en Ciencias de 1.° a 3.° básico. Ya era una decisión pendiente del dueño (D).
6. **Detalles de redacción:** 5.° básico Mat OA 6 y OA 13 (ejemplos confusos), Lenguaje OA 5 (poema sin rima), 2.° básico
   (ardilla, que no es fauna chilena).

### Prioridad sugerida si se decide corregir

| Prioridad | Qué | Por qué |
|---|---|---|
| 1 | 2.° medio función cuadrática; 8.° básico ecuaciones e inecuaciones | Contenido central del examen, hoy sin ejemplos suficientes |
| 2 | Inglés: vocabulario temático (5.° básico a 2.° medio) | Brecha presente en 6 cursos |
| 3 | Faltas parciales puntuales: pirámide y cilindro (2.°), áreas irregulares (5.°), planetas (1.° medio), populismos Brasil y México (2.° medio), recursivas (8.°) | Indicador oficial no enseñado |
| 4 | Ejemplos de «crear problema/patrón», números en palabras, algoritmo vertical | Indicadores débiles en básica |
| 5 | Figuras y mapas con los marcadores existentes; preguntas de práctica de Matemática | Mejoran la comprensión; no faltan contenidos |
| 6 | `[Imagen]` y redacción | Decisión D del dueño / detalles |

## Correcciones aplicadas (2026-11-17)

Hechas en `main` (commits `c58e4d6`, `03735c4`, `dec69af` y el siguiente), con `scripts/correccion/insertar.py`:

- **Prioridad 1:**
  - 2.° medio OA 3: parábola graficada, efecto de a/b/c, problemas con ecuación cuadrática (terreno, lanzamiento), discriminante y región de la inecuación.
  - 2.° medio OA 5: gráfica de la inversa y un problema.
  - 8.° básico OA 8: las 7 formas de ecuación más inecuaciones.
  - 8.° básico OA 10: recta desde dos puntos y forma recursiva.
  - 8.° básico OA 3: potencia de potencia. OA 12: despeje general y Pitágoras en 3D.
- **Prioridad 2:** tabla de vocabulario temático del temario, con traducción y un ejemplo, en Inglés de 5.° básico a 2.° medio.
- **Prioridad 3:** pirámide y cilindro (2.° básico), áreas irregulares (5.°), tabla comparativa de planetas (1.° medio CN OA 14), populismos de Perón, Vargas y Cárdenas por criterios (2.° medio).
- **Prioridad 4:**
  - crear problemas (1.° y 2.° básico) y patrones (2.° y 3.°);
  - tablas pictóricas (3.°);
  - en 4.° básico: números en palabras y orden, algoritmo vertical de multiplicación y división, y fracciones con figura.
- **Prioridad 5:**
  - Mapas nuevos: expansión territorial (6.°), independencias con línea de tiempo (8.°), Estados del siglo XIX y territorio de Chile (1.° medio).
  - Varios mapas de básica que el análisis marcó como faltantes ya existían en preguntas o ejemplos.
  - +8 preguntas de práctica (inecuaciones, recursiva, cuadrática).
- **Débiles y redacción:**
  - agrupar seres vivos (1.°), normas cotidianas (5.°), rima con ejemplo real (5.° Lenguaje OA 5);
  - ejemplos confusos de 5.° Mat OA 6 y OA 13 reescritos;
  - la ardilla se reemplaza por el monito del monte (2.°);
  - peste negra con gráfico (7.° Hist OA 12), leer un gráfico y problema algebraico (7.° Mat);
  - ley de Joule (8.° CN OA 10), consecuencias sociales del neoliberalismo (2.° medio).

Verificación: reimportación OK (410 OA, 6.689 preguntas, 0 sin OA), guardas de contenido en pytest en verde, validación en la app
de 8.° básico (29/29) y 2.° medio (24/24). Los tests de conteo se actualizaron: estaban desfasados por los 20 simulacros Forma A.

**Segunda tanda (2026-11-17), cierra los pendientes menores:**
- **Dibujos nuevos en la app:**
  - mapa `mundo` (Natural Earth, con `lineas=si` para el Ecuador, los trópicos y los círculos polares, y `pintar2=` para un segundo color);
  - regiones de Chile (`regiones=si`, límites aproximados);
  - marcador `::plano::` (plano cartesiano con polígonos, circunferencias, puntos y rayos). Tiene tests en `markdown-marcadores.spec.ts`.
- **Usados en:**
  - continentes, océanos y zonas climáticas (3.° básico OA 7 y 8);
  - regiones (6.° básico OA 11);
  - Guerra Fría (2.° medio OA 8);
  - ángulo central e inscrito y cuerdas que se cortan (3.° medio OA 4);
  - homotecia con k = 2 y k = −½ (1.° medio OA 8);
  - función seno (4.° medio OA 3);
  - gráficos posición–tiempo y velocidad–tiempo, y adición de velocidades de Galileo (2.° medio CN OA 9);
  - balanza dibujada (6.° básico OA 11).
- **Ítems débiles restantes:**
  - g ↔ kg (3.°), ordenar listas (5.°), población por zona natural (5.° Hist OA 9);
  - raíz en ciencias (8.°) e impacto económico y científico de la Conquista (8.° Hist OA 7);
  - en 1.° medio: crecimiento con potencias, completar el cuadrado, astronomía de pueblos originarios y consecuencias de la Primera Guerra Mundial;
  - en 2.° medio: golpes de Estado comparados, categorías de discriminación y soluciones en los tres estados.
- **Inglés:**
  - organizadores e idea principal en OA 10 (7.° básico a 2.° medio);
  - preferencias en OA 13 (8.° básico a 2.° medio);
  - ubicaciones en la ciudad (6.° básico);
  - +11 preguntas de banco.
- **Práctica de Matemática:** +28 preguntas en las pruebas de unidad de 1.° a 6.° básico, una por cada OA que tenía poca práctica.

**Sigue pendiente:**
- `[Imagen]` (decisión D);
- la práctica moderada de Matemática en media (3.° y 4.° medio): está cubierta, pero podría ampliarse.
