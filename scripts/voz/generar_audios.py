"""Genera los audios pregrabados con Piper (voz es_MX-claude-high, Apache-2.0).

Uso: python generar_audios.py <textos.json> <modelo.onnx> <espeak-ng-data> <salida/>
Solo genera los que faltan y reescribe manifest.json con todas las claves presentes.
Requiere macOS (afconvert) o ffmpeg para codificar a AAC mono 32 kbps (.m4a)."""
import json
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from piper import PiperVoice, SynthesisConfig

VOZ = "piper/es_MX-claude-high"
PAUSA_ENTRE_FRASES_S = 0.35
# Un poco más lento que lo normal: el público son niños y niñas de 6 a 8 años.
CONFIG = SynthesisConfig(length_scale=1.08)


def codificar(wav: Path, destino: Path) -> None:
    if shutil.which("afconvert"):
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "32000", str(wav), str(destino)], check=True)
    else:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-c:a", "aac",
                        "-b:a", "32k", str(destino)], check=True)


def main() -> None:
    textos = json.loads(Path(sys.argv[1]).read_text())
    voz = PiperVoice.load(sys.argv[2], espeak_data_dir=sys.argv[3])
    salida = Path(sys.argv[4])
    salida.mkdir(parents=True, exist_ok=True)
    nuevos = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(textos, 1):
            destino = salida / f"{t['clave']}.m4a"
            if destino.exists():
                continue
            partes, sr = [], voz.config.sample_rate
            for trozo in voz.synthesize(t["texto"], syn_config=CONFIG):
                partes += [trozo.audio_int16_array, np.zeros(int(sr * PAUSA_ENTRE_FRASES_S), dtype=np.int16)]
            wav = Path(tmp) / "a.wav"
            with wave.open(str(wav), "wb") as w:
                w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr)
                w.writeframes(np.concatenate(partes).tobytes())
            codificar(wav, destino)
            nuevos += 1
            if i % 100 == 0:
                print(f"  {i}/{len(textos)}", flush=True)
    claves = sorted(p.stem for p in salida.glob("*.m4a"))
    (salida / "manifest.json").write_text(json.dumps({"voz": VOZ, "claves": claves}))
    print(f"{nuevos} audios nuevos; {len(claves)} en total en {salida}")


if __name__ == "__main__":
    main()
