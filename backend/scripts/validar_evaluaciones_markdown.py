"""Validaciones estáticas conservadoras para evaluaciones Markdown.

Detecta claves en tablas de pauta y declaraciones explícitas de puntaje total.
No reemplaza revisión pedagógica ni inspección de recursos renderizados.
"""
from __future__ import annotations

import re
from pathlib import Path

OPTION_RE = re.compile(r"^\s*([a-d])\)\s*(.*?)\s*$", re.IGNORECASE)
TOTAL_RE = re.compile(r"(?i)puntaje\s+total\s*: ?\s*(\d+)\s*puntos?")
QUESTION_RE = re.compile(r"^\s*\*{0,2}(?:Pregunta\s+)?(\d+)\.?\*{0,2}")
TABLE_KEY_RE = re.compile(r"(?i)\*{0,2}([a-d])\)\s*(.+?)\*{0,2}[.]?\s*$")


def _question_options(markdown: str) -> dict[int, dict[str, str]]:
    questions: dict[int, dict[str, str]] = {}
    current: int | None = None
    for line in markdown.splitlines():
        qmatch = QUESTION_RE.match(line)
        if qmatch:
            current = int(qmatch.group(1))
            questions.setdefault(current, {})
            continue
        if current is not None:
            option = OPTION_RE.match(line)
            if option:
                questions[current][option.group(1).lower()] = option.group(2).strip()
            elif line.strip() in {"---", "***"}:
                current = None
    return questions


def check_key_option_consistency(markdown: str, path: str = "<memoria>") -> list[str]:
    """Compara claves a)/b)/c)/d) en filas de pauta con las opciones de la pregunta."""
    options_by_question = _question_options(markdown)
    findings: list[str] = []
    for line_no, line in enumerate(markdown.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].isdigit():
            continue
        question_no = int(cells[0])
        # Las tablas de pauta del repositorio usan: N° | Asignatura | Clave/criterio | OA.
        key_cell = cells[2].strip().strip("*_ ")
        match = TABLE_KEY_RE.match(key_cell)
        if not match:
            continue
        letter, answer = match.group(1).lower(), match.group(2).strip().strip("*_ ")
        options = options_by_question.get(question_no, {})
        if not options:
            continue
        if letter not in options:
            findings.append(
                f"{path}:{line_no}: pregunta {question_no}: la clave refiere a {letter}), "
                f"pero las opciones disponibles son {', '.join(sorted(options))}"
            )
            continue
        norm = lambda value: re.sub(r"\s+", " ", value).casefold().rstrip(".")
        if norm(answer) != norm(options[letter]):
            findings.append(
                f"{path}:{line_no}: pregunta {question_no}: la clave {letter}) {answer} "
                f"no coincide con la alternativa {letter}) {options[letter]}"
            )
    return findings


def check_conflicting_total_declarations(markdown: str, path: str = "<memoria>") -> list[str]:
    values = [int(match.group(1)) for match in TOTAL_RE.finditer(markdown)]
    distinct = sorted(set(values))
    if len(distinct) <= 1:
        return []
    return [f"{path}: declaraciones de puntaje total incompatibles: " +
            ", ".join(f"{value} puntos" for value in distinct)]


def audit_file(path: Path) -> list[str]:
    try:
        markdown = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: no se pudo leer: {exc}"]
    return check_key_option_consistency(markdown, str(path)) + check_conflicting_total_declarations(markdown, str(path))


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    files = sorted((root / "contenido").rglob("*.md"))
    findings = [finding for path in files for finding in audit_file(path)]
    if findings:
        print("\n".join(findings))
        print(f"\nHallazgos estructurales: {len(findings)}")
        return 1
    print(f"Sin discrepancias detectadas por estos controles en {len(files)} archivos Markdown.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
