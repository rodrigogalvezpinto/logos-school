/**
 * Prepara los textos que el botón «Escuchar» leerá, con la MISMA limpieza que usa la app
 * (texto-para-voz.ts) y su clave de audio. Lo usa scripts/voz/generar_audios.sh.
 * Entrada: JSON { guias: string[], preguntas: {tipo, enunciado, opciones}[] }.
 * Salida: JSON [{ clave, texto }] sin repetidos.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { textoParaVoz, textoPreguntaParaVoz, PreguntaParaVoz } from '../src/app/shared/texto-para-voz';
import { claveAudio } from '../src/app/core/audio-pregrabado';

const entrada = JSON.parse(readFileSync(process.argv[2], 'utf-8')) as { guias: string[]; preguntas: PreguntaParaVoz[] };
// El botón vuelve a pasar el texto por textoParaVoz: la clave se calcula sobre el texto final.
const textos = [...entrada.guias.map((g) => textoParaVoz(g)), ...entrada.preguntas.map((p) => textoParaVoz(textoPreguntaParaVoz(p)))];
const unicos = new Map<string, string>();
for (const texto of textos) if (texto) unicos.set(claveAudio(texto), texto);
writeFileSync(process.argv[3], JSON.stringify([...unicos].map(([clave, texto]) => ({ clave, texto }))));
console.log(`${unicos.size} textos únicos → ${process.argv[3]}`);
