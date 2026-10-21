"""Validaciones estáticas conservadoras para evaluaciones Markdown.

Solo reporta patrones estructurales verificables; no reemplaza revisión pedagógica
ni inspección de recursos renderizados.
"""
from __future__ import annotations

import re
from pathlib import Path

OPTION_RE = re.compile(r"^\s*([a-d])\)\s*(.*?)\s*$", re.IGNORECASE)
KEY_RE = re.compile(
    r"(?i)(?:respuesta\s+(?:correcta|esperada)|clave)\s*:?\s*[*_ ]*([a-d])\)\s*(.+?)\s*[*_]*$"
)
TOTAL_RE = re.compile(r"(?i)puntaje\s+total\s*:?\s*(\d+)\s*puntos?")


def check_key_option_consistency(markdown: str, path: str = "<memoria>") -> list[str]:
    """Detecta claves del tipo 'Respuesta correcta: c) 14' cuyo texto no está en esa opción."""
    findings: list[str] = []
    lines = markdown.splitlines()
    for idx, line in enumerate(lines):
        match = KEY_RE.search(line.strip().strip("*_ "))
        if not match:
            continue
        key_letter, key_text = match.group(1).lower(), match.group(2).strip().strip("*_ ")
        # Busca opciones en el bloque local de la pregunta; corta en separador o nueva pregunta.
        start = idx
        while start > 0 and lines[start - 1].strip() not in {"---", "***"} and not re.match(r"^\s*\*{0,2}\d+\.", lines[start - 1]):
            start -= 1
        end = idx + 1
        while end < len(lines) and lines[end].strip() not in {"---", "***"} and not re.match(r"^\s*\*{0,2}\d+\.", lines[end]):
            end += 1
        options: dict[str, str] = {}
        for candidate in lines[start:end]:
            option = OPTION_RE.match(candidate)
            if option:
                options[option.group(1).lower()] = option.group(2).strip()
        if options and key_letter in options:
            normalized_key = re.sub(r"\s+", " ", key_text).casefold().rstrip(".")
            normalized_option = re.sub(r"\s+", " ", options[key_letter]).casefold().rstrip(".")
            if normalized_key != normalized_option:
                findings.append(
                    f"{path}:{idx + 1}: la clave {key_letter}) {key_text} no coincide "
                    f"con la alternativa {key_letter}) {options[key_letter]}"
                )
        elif options and key_letter not in options:
            findings.append(
                f"{path}:{idx + 1}: la clave refiere a {key_letter}), "
                f"pero las opciones disponibles son {', '.join(sorted(options))}"
            )
    return findings


def check_conflicting_total_declarations(markdown: str, path: str = "<memoria>") -> list[str]:
    """Detecta dos o más declaraciones explícitas de puntaje total que difieren."""
    values = [(int(m.group(1)), m.start()) for m in TOTAL_RE.finditer(markdown)]
    distinct = sorted({value for value, _ in values})
    if len(distinct) <= 1:
        return []
    return [
        f"{path}: declaraciones de puntaje total incompatibles: "
        + ", ".join(f"{value} puntos" for value in distinct)
    ]


def audit_file(path: Path) -> list[str]:
    try:
        markdown = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: no se pudo leer: {exc}"]
    return (
        check_key_option_consistency(markdown, str(path))
        + check_conflicting_total_declarations(markdown, str(path))
    )


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    content_root = root / "contenido"
    files = sorted(content_root.rglob("*.md"))
    findings = [finding for path in files for finding in audit_file(path)]
    if findings:
        print("\n".join(findings))
        print(f"\nHallazgos estructurales: {len(findings)}")
        return 1
    print(f"Sin discrepancias detectadas por estos controles en {len(files)} archivos Markdown.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
