"""Seed del Plan Lector, de 1.° básico a 4.° medio (piloto en 4.° básico: 2026-08-15; los 12 cursos: 2026-11-22).

Libros reales, de lectura habitual en colegios chilenos, elegidos con criterio pedagógico por edad
(planificacion/04-modo-de-operacion.md). La editorial se deja como «Cualquier edición completa»: casi todos tienen
varias ediciones y para estudiar da lo mismo cuál se use (lo que importa es que no sea una versión resumida).
Idempotente: reemplaza la lista de cada nivel.

Uso: python scripts/seed_plan_lector.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import LibroPlanLector, Nivel

EDICION = "Cualquier edición completa"

# nivel -> [(título, autor)]
LIBROS = {
    "1° básico": [
        ("La polilla del baúl", "Mario Carvajal y Carlos Saraniti"),
        ("¡Ay, cuánto me quiero!", "Mauricio Paredes"),
        ("El monstruo de colores", "Anna Llenas"),
        ("Choco encuentra una mamá", "Keiko Kasza"),
    ],
    "2° básico": [
        ("La cama mágica de Bartolo", "Mauricio Paredes"),
        ("El lugar más bonito del mundo", "Ann Cameron"),
        ("Ámbar en cuarto y sin su amigo", "Paula Danziger"),
        ("El secuestro de la bibliotecaria", "Margaret Mahy"),
    ],
    "3° básico": [
        ("La porota", "Hernán del Solar"),
        ("Efraín en la vega", "Mario Carvajal"),
        ("El superzorro", "Roald Dahl"),
        ("Cuentos de la selva", "Horacio Quiroga"),
    ],
    "4° básico": [
        ("Papelucho", "Marcela Paz"),
        ("Matilda", "Roald Dahl"),
        ("Charlie y la fábrica de chocolate", "Roald Dahl"),
        ("Ritalinda", "Beatriz Rojas"),
    ],
    "5° básico": [
        ("El Principito", "Antoine de Saint-Exupéry"),
        ("Quique Hache, detective", "Sergio Gómez"),
        ("Las crónicas de Narnia: El león, la bruja y el ropero", "C. S. Lewis"),
        ("Mi planta de naranja-lima", "José Mauro de Vasconcelos"),
    ],
    "6° básico": [
        ("Mac, el microbio desconocido", "Hernán del Solar"),
        ("Las aventuras de Tom Sawyer", "Mark Twain"),
        ("Corazón", "Edmondo De Amicis"),
        ("Harry Potter y la piedra filosofal", "J. K. Rowling"),
    ],
    "7° básico": [
        ("Frin", "Luis María Pescetti"),
        ("El diario de Ana Frank", "Ana Frank"),
        ("El caballero de la armadura oxidada", "Robert Fisher"),
        ("Subterra", "Baldomero Lillo"),
    ],
    "8° básico": [
        ("Cuentos de amor, de locura y de muerte", "Horacio Quiroga"),
        ("Narraciones extraordinarias", "Edgar Allan Poe"),
        ("Romeo y Julieta", "William Shakespeare"),
        ("El niño con el pijama de rayas", "John Boyne"),
    ],
    "1° medio": [
        ("Lazarillo de Tormes", "Anónimo"),
        ("Edipo rey", "Sófocles"),
        ("La metamorfosis", "Franz Kafka"),
        ("Fahrenheit 451", "Ray Bradbury"),
    ],
    "2° medio": [
        ("Crónica de una muerte anunciada", "Gabriel García Márquez"),
        ("Rebelión en la granja", "George Orwell"),
        ("Bodas de sangre", "Federico García Lorca"),
        ("Hijo de ladrón", "Manuel Rojas"),
    ],
    "3° medio": [
        ("El túnel", "Ernesto Sabato"),
        ("1984", "George Orwell"),
        ("Casa de muñecas", "Henrik Ibsen"),
        ("Ardiente paciencia", "Antonio Skármeta"),
    ],
    "4° medio": [
        ("Pedro Páramo", "Juan Rulfo"),
        ("La casa de los espíritus", "Isabel Allende"),
        ("Un mundo feliz", "Aldous Huxley"),
        ("Veinte poemas de amor y una canción desesperada", "Pablo Neruda"),
    ],
}


def main() -> None:
    with Session(engine) as session:
        total = 0
        for nombre_nivel, libros in LIBROS.items():
            nivel = session.exec(select(Nivel).where(Nivel.nombre == nombre_nivel)).first()
            if not nivel:
                print(f"No se encontró el nivel {nombre_nivel} — importar el contenido primero.")
                continue
            for libro in session.exec(select(LibroPlanLector).where(LibroPlanLector.nivel_id == nivel.id)).all():
                session.delete(libro)
            session.commit()
            for i, (titulo, autor) in enumerate(libros, start=1):
                session.add(LibroPlanLector(nivel_id=nivel.id, orden=i, titulo=titulo, autor=autor, editorial=EDICION))
            session.commit()
            total += len(libros)
        print(f"Plan Lector: {total} libros en {len(LIBROS)} cursos.")


if __name__ == "__main__":
    main()
