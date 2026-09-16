from app.infrastructure.pdf.sanitizar_texto import sanitizar_para_pdf


def test_flecha_derecha_se_reemplaza_en_vez_de_desaparecer():
    """Bug real: la fuente Helvetica core no tiene '→' (fuera de latin-1) — sin un
    reemplazo explícito, la última red de seguridad la descartaba en silencio, dejando un
    hueco de doble espacio en vez de una flecha visible (ej. contenido/03-basico/
    matematica.md usa '→' para mostrar "7 está en la posición de las unidades de mil →
    vale 7.000")."""
    resultado = sanitizar_para_pdf("unidades de mil → vale 7.000")
    assert "->" in resultado
    assert "  " not in resultado


def test_em_dash_y_tildes_se_preservan_o_reemplazan_sin_romper():
    resultado = sanitizar_para_pdf("Recuerda — la idea principal está al final.")
    assert resultado == "Recuerda - la idea principal está al final."
