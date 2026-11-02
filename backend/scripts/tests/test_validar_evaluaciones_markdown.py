from pathlib import Path

from scripts.validar_evaluaciones_markdown import (
    check_conflicting_total_declarations,
    check_key_option_consistency,
    check_reused_exam_stimuli,
)


def test_detecta_escala_de_notas_incompatible_con_exigencia_declarada():
    from scripts.validar_evaluaciones_markdown import check_grade_scale_consistency

    texto = """**Puntaje total:** 37 puntos
| Puntaje obtenido | Nota aproximada (exigencia 60%) |
|---|---|
| 26-32 pts | 5,2 - 6,1 |
"""
    hallazgos = check_grade_scale_consistency(texto, "historia.md")
    assert len(hallazgos) == 1
    assert "4.8" in hallazgos[0] and "6.0" in hallazgos[0]
    assert "historia.md:4" in hallazgos[0]


def test_acepta_escalas_de_notas_concordantes_con_motor():
    from app.domain.evaluaciones.value_objects import calcular_nota
    from scripts.validar_evaluaciones_markdown import check_grade_scale_consistency

    for total in (34, 35, 37):
        filas = [f"| {p}-{p} pts | {calcular_nota(p, total):.1f} - {calcular_nota(p, total):.1f} |"
                 for p in range(total + 1)]
        texto = f"Puntaje total: {total} puntos\n| Puntaje obtenido | Nota (exigencia 60%) |\n|---|---|\n" + "\n".join(filas)
        assert check_grade_scale_consistency(texto) == []
    assert check_grade_scale_consistency("Una nota al pie sin escala numérica.") == []


def test_escala_sin_total_verificable_se_informa():
    from scripts.validar_evaluaciones_markdown import check_grade_scale_consistency

    texto = "| Puntaje obtenido | Nota (exigencia 60%) |\n|---|---|\n| 0-10 pts | 1,0 - 3,0 |"
    assert len(check_grade_scale_consistency(texto)) == 1


def test_guia_ingles_5b_no_conserva_puntuacion_residual_en_pauta_postal():
    guia = Path(__file__).resolve().parents[3] / "contenido/05-basico/ingles.md"
    texto = guia.read_text(encoding="utf-8")
    assert "**Respuesta correcta:** b) From,." not in texto
    assert "**Respuesta correcta:** b) From." in texto


def test_detecta_estimulo_largo_reutilizado_con_saltos_de_linea():
    guia = 'Read: *"My sister has a new blue pencil case."*'
    examen = 'Read: "My sister has a new\nblue pencil case."'
    assert check_reused_exam_stimuli(examen, guia) == [
        "my sister has a new blue pencil case"
    ]


def test_no_confunde_formula_breve_con_estimulo_reutilizado():
    assert check_reused_exam_stimuli('"Thank you."', '"Thank you."') == []
    assert check_reused_exam_stimuli(
        '"My sister has a new blue pencil case."',
        '"My brother has a new red pencil case."',
    ) == []


def test_simulacro_ingles_5b_no_copia_estimulos_largos_de_la_guia():
    curso = Path(__file__).resolve().parents[3] / "contenido/05-basico"
    guia = (curso / "ingles.md").read_text(encoding="utf-8")
    examen = (curso / "examenes/ingles-examen-forma-b.md").read_text(encoding="utf-8")
    assert check_reused_exam_stimuli(examen, guia) == []
    assert check_key_option_consistency(examen) == []


def test_detecta_clave_que_no_coincide_con_alternativa():
    markdown = """**16. Resuelve x + 9 = 23.**
a) 32
b) 14
c) 13
d) 15
Respuesta correcta: c) 14
"""
    findings = check_key_option_consistency(markdown, "ejemplo.md")
    assert len(findings) == 1
    assert "clave c) 14 no coincide" in findings[0]
    assert "alternativa c) 13" in findings[0]


def test_acepta_clave_coherente():
    markdown = """**16. Resuelve x + 9 = 23.**
a) 32
b) 14
c) 13
d) 15
Respuesta correcta: b) 14
"""
    assert check_key_option_consistency(markdown) == []


def test_detecta_totales_declarados_incompatibles():
    markdown = "Puntaje total: 30 puntos\n...\nPuntaje total: 35 puntos"
    findings = check_conflicting_total_declarations(markdown, "historia.md")
    assert len(findings) == 1
    assert "30 puntos" in findings[0]
    assert "35 puntos" in findings[0]


def test_no_inventa_discrepancia_si_solo_hay_un_total():
    assert check_conflicting_total_declarations("Puntaje total: 35 puntos") == []


def test_palabra_alternativas_en_texto_comun_no_es_clave():
    markdown = "Compara las alternativas de ahorro que ofrece el banco."
    assert check_key_option_consistency(markdown) == []



def test_detecta_clave_incorrecta_en_tabla_de_pauta_real():
    markdown = """**16. (Matemática)** Resuelve x + 9 = 23.
a) 32
b) 14
c) 13
d) 15

---

# PAUTA DE CORRECCIÓN
| N° | Asignatura | Clave / criterio de respuesta correcta | Objetivo |
|----|------------|----------------------------------------|----------|
| 16 | Matemática | **c) 14.** Para despejar x se resta 9 a ambos lados. | OA 14 |
"""
    findings = check_key_option_consistency(markdown, "examen.md")
    assert len(findings) == 1
    assert "pregunta 16" in findings[0]
    assert "c) 14" in findings[0]
    assert "c) 13" in findings[0]


def test_acepta_clave_correcta_en_tabla_de_pauta():
    markdown = """**16. (Matemática)** Resuelve x + 9 = 23.
a) 32
b) 14
c) 13
d) 15

---

| N° | Asignatura | Clave / criterio de respuesta correcta | Objetivo |
|----|------------|----------------------------------------|----------|
| 16 | Matemática | **b) 14.** Para despejar x se resta 9 a ambos lados. | OA 14 |
"""
    assert check_key_option_consistency(markdown) == []



def test_detecta_totales_con_negrita_markdown():
    markdown = "**Puntaje total:** 30 puntos\n...\n**Puntaje total: 35 puntos**"
    findings = check_conflicting_total_declarations(markdown, "historia.md")
    assert len(findings) == 1
    assert "30 puntos" in findings[0]
    assert "35 puntos" in findings[0]


def test_detecta_clave_en_segunda_columna_de_tabla():
    markdown = """**Pregunta 14.** ¿Cuál es la inversa de f(x) = x + 10?
a) f⁻¹(x) = x − 10
b) f⁻¹(x) = x + 10
c) f⁻¹(x) = 10 − x
d) f⁻¹(x) = −x − 10

---

## PAUTA DE CORRECCIÓN
| N° | Clave / Respuesta esperada | OA | Eje |
|---|---|---|---|
| 14 | **a) f⁻¹(x) = x + 10** (explicación contradictoria) | OA 5 | Álgebra |
"""
    findings = check_key_option_consistency(markdown, "matematica-2m.md")
    assert len(findings) == 1
    assert "pregunta 14" in findings[0]
    assert "clave a)" in findings[0]
    assert "alternativa a)" in findings[0]
