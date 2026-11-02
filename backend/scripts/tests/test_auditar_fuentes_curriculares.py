from scripts.auditar_fuentes_curriculares import extraer_oa, paginas_ingles


def test_incluye_continuacion_sin_repetir_encabezado():
    paginas = ["Matemática OA 1", "Idioma Extranjero: Inglés OA N°5", "OA N°8", "Vocabulario"]
    assert paginas_ingles(paginas) == [2, 3, 4]


def test_no_inventa_seccion_si_no_hay_encabezado():
    assert paginas_ingles(["Historia OA 1", "Bibliografía"]) == []


def test_extrae_objetivos_sin_duplicar_numeros_de_ejemplos():
    assert extraer_oa("OA N°5; OA N°6; OA 5; 25 preguntas; Objetivo de Aprendizaje 14") == [5, 6, 14]
