"""Validaciones estáticas conservadoras para evaluaciones Markdown.
Detecta discrepancias entre claves explícitas y alternativas, y declaraciones
incompatibles de puntaje total. No reemplaza revisión pedagógica ni de recursos.
"""
from __future__ import annotations
import re
from pathlib import Path

OPTION_RE = re.compile(r"^\s*([a-d])\)\s*(.*?)\s*$", re.IGNORECASE)
TOTAL_RE = re.compile(r"(?i)puntaje\s+total\s*:\s*(\d+)\s*puntos?")
QUESTION_RE = re.compile(r"^\s*\*{0,2}(?:Pregunta\s+)?(\d+)\.?")
INLINE_KEY_RE = re.compile(r"(?i)respuesta\s+correcta\s*:\s*\*{0,2}([a-d])\)\s*(.+?)\*{0,2}\s*$")
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
            elif line.strip() in {"---", "***"} or line.lstrip().startswith("# "):
                current = None
    return questions


def _normalise(value: str) -> str:
    value = re.sub(r"[*_]", "", value)
    return re.sub(r"\s+", " ", value).strip().casefold().rstrip(".").strip()


def _compare(question_no: int, letter: str, answer: str,
             options_by_question: dict[int, dict[str, str]], path: str,
             line_no: int) -> list[str]:
    options = options_by_question.get(question_no, {})
    if not options:
        return []
    letter = letter.lower()
    answer = answer.strip().strip("*_ ").rstrip(".").strip()
    if letter not in options:
        return [f"{path}:{line_no}: pregunta {question_no}: la clave refiere a {letter}), "
                f"pero las opciones disponibles son {', '.join(sorted(options))}"]
    if _normalise(answer) != _normalise(options[letter]):
        return [f"{path}:{line_no}: pregunta {question_no}: la clave {letter}) {answer} "
                f"no coincide con la alternativa {letter}) {options[letter]}"]
    return []


def check_key_option_consistency(markdown: str, path: str = "<memoria>") -> list[str]:
    """Compara claves explícitas en texto o tablas con las opciones de cada pregunta."""
    options_by_question = _question_options(markdown)
    findings: list[str] = []
    current_question: int | None = None
    for line_no, line in enumerate(markdown.splitlines(), start=1):
        qmatch = QUESTION_RE.match(line)
        if qmatch:
            current_question = int(qmatch.group(1))
        inline = INLINE_KEY_RE.search(line)
        if inline and current_question is not None:
            findings.extend(_compare(current_question, inline.group(1), inline.group(2),
                                     options_by_question, path, line_no))
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].isdigit():
            continue
        question_no = int(cells[0])
        match = TABLE_KEY_RE.match(cells[2].strip().strip("*_ "))
        if match:
            findings.extend(_compare(question_no, match.group(1), match.group(2),
                                     options_by_question, path, line_no))
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
    return (check_key_option_consistency(markdown, str(path)) +
            check_conflicting_total_declarations(markdown, str(path)))


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
