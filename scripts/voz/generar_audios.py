"""Genera los audios pregrabados con Kokoro (voz em_alex, modelo Kokoro-82M, Apache-2.0).

Voz elegida por el usuario el 2026-11-07 tras comparar 8 voces libres (ver
planificacion/21-accesibilidad-lectura-y-contenido-visual.md).

Uso: python generar_audios.py <textos.json> <kokoro.onnx> <voices.bin> <salida/>
Solo genera los que faltan (LIMPIAR_HUERFANOS=1 borra los que ya no corresponden a ningún
texto; usarlo solo con la lista completa de niveles) y reescribe manifest.json con todas las claves presentes. Si la
carpeta tiene audios de otra voz, los borra primero (la clave depende solo del texto).
Requiere macOS (afconvert) o ffmpeg para codificar a AAC mono 32 kbps (.m4a)."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from kokoro_onnx import Kokoro

VOZ = "kokoro/em_alex"
VELOCIDAD = 0.95  # la misma de la muestra elegida; un poco más pausada para niños de 6 a 8 años
PAUSA_ENTRE_FRASES_S = 0.3
MAX_CARACTERES = 300


def frases(texto: str) -> list[str]:
    """Trozos cortos por frase: pausas naturales y entradas dentro del límite del modelo."""
    trozos, actual = [], ""
    for f in re.split(r"(?<=[.!?;:])\s+", texto.strip()):
        if actual and len(actual) + len(f) + 1 > MAX_CARACTERES:
            trozos.append(actual)
            actual = f
        else:
            actual = f"{actual} {f}".strip()
    if actual:
        trozos.append(actual)
    return trozos


def codificar(wav: Path, destino: Path) -> None:
    if shutil.which("afconvert"):
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "32000", str(wav), str(destino)], check=True)
    else:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-c:a", "aac",
                        "-b:a", "32k", str(destino)], check=True)


def main() -> None:
    textos = json.loads(Path(sys.argv[1]).read_text())
    kokoro = Kokoro(sys.argv[2], sys.argv[3])
    salida = Path(sys.argv[4])
    salida.mkdir(parents=True, exist_ok=True)
    manifiesto = salida / "manifest.json"
    if manifiesto.exists() and json.loads(manifiesto.read_text()).get("voz") != VOZ:
        for viejo in salida.glob("*.m4a"):
            viejo.unlink()
    if os.environ.get("LIMPIAR_HUERFANOS") == "1":
        # Solo con la lista COMPLETA de niveles: borra audios cuyo texto cambió o ya no existe.
        vigentes = {t["clave"] for t in textos}
        for huerfano in salida.glob("*.m4a"):
            if huerfano.stem not in vigentes:
                huerfano.unlink()
    nuevos = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(textos, 1):
            destino = salida / f"{t['clave']}.m4a"
            if destino.exists():
                continue
            partes, sr = [], 24000
            for frase in frases(t["texto"]):
                audio, sr = kokoro.create(frase, voice="em_alex", speed=VELOCIDAD, lang="es")
                partes += [audio, np.zeros(int(sr * PAUSA_ENTRE_FRASES_S), dtype=np.float32)]
            pcm = (np.clip(np.concatenate(partes), -1, 1) * 32767).astype(np.int16)
            wav = Path(tmp) / "a.wav"
            with wave.open(str(wav), "wb") as w:
                w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr)
                w.writeframes(pcm.tobytes())
            codificar(wav, destino)
            nuevos += 1
            if i % 50 == 0:
                print(f"  {i}/{len(textos)}", flush=True)
    claves = sorted(p.stem for p in salida.glob("*.m4a"))
    manifiesto.write_text(json.dumps({"voz": VOZ, "claves": claves}))
    print(f"{nuevos} audios nuevos; {len(claves)} en total en {salida}")


if __name__ == "__main__":
    main()
