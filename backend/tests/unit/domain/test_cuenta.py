from app.domain.auth.entities import Cuenta


def test_crear_con_password_no_tiene_google_id():
    cuenta = Cuenta.crear_con_password(email="a@test.cl", nombre="A", password_hash="hash")
    assert cuenta.id is None
    assert cuenta.google_id is None
    assert cuenta.password_hash == "hash"


def test_crear_con_google_no_tiene_password():
    cuenta = Cuenta.crear_con_google(email="a@test.cl", nombre="A", google_id="g-123")
    assert cuenta.password_hash is None
    assert cuenta.google_id == "g-123"


def test_vincular_google_asigna_el_google_id():
    cuenta = Cuenta.crear_con_password(email="a@test.cl", nombre="A", password_hash="hash")
    cuenta.vincular_google("g-456")
    assert cuenta.google_id == "g-456"
