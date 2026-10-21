from scripts.validar_evaluaciones_markdown import (
    check_conflicting_total_declarations,
    check_key_option_consistency,
)


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
