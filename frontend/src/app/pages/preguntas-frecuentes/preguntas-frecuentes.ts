import { Component, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

interface Pregunta {
  pregunta: string;
  respuesta: string;
  categoria: 'logos' | 'tramite';
}

@Component({
  selector: 'app-preguntas-frecuentes',
  standalone: true,
  imports: [RouterLink, Logo],
  templateUrl: './preguntas-frecuentes.html',
  styleUrl: './preguntas-frecuentes.scss',
})
export class PreguntasFrecuentes {
  abierta = signal<number | null>(0);

  preguntas: Pregunta[] = [
    {
      categoria: 'logos',
      pregunta: '¿Logos School tiene material suficiente para preparar a mi hijo/a para el examen libre?',
      respuesta:
        'Sí. Cubrimos el temario oficial completo que exige el Mineduc para el curso de tu hijo/a, objetivo por objetivo. Incluye la materia explicada con ejemplos, cientos de preguntas de práctica, pruebas cortas por unidad, y un examen de práctica idéntico en formato al examen real.',
    },
    {
      categoria: 'logos',
      pregunta: '¿Cómo es la modalidad de evaluación dentro de Logos School?',
      respuesta:
        'Tres niveles: práctica libre (sin nota, feedback inmediato), pruebas de unidad (con nota, sin cronómetro) y examen simulacro (cronometrado, mismo formato del examen real — es la mejor señal de si está listo).',
    },
    {
      categoria: 'logos',
      pregunta: '¿Cómo voy a ir viendo el avance de mi hijo/a?',
      respuesta:
        'Vas a tener un panel con las notas por materia, el historial de todo lo rendido, y el resultado del examen simulacro destacado como la referencia más confiable de preparación real — distinto de las notas de práctica.',
    },
    {
      categoria: 'logos',
      pregunta: '¿Logos School es gratis?',
      respuesta:
        'Logos School tiene planes de pago accesibles (desde $19.990 CLP mensual, con opciones por periodo de examinación o anual con descuento) — no es un colegio online tradicional con mensualidades altas, está pensado para ser una alternativa accesible.',
    },
    {
      categoria: 'tramite',
      pregunta: '¿Es un solo examen al año, en octubre?',
      respuesta:
        'No. Hay 3 periodos de examinación: Periodo 1 (abril-junio, todos los cursos), Periodo 2 (septiembre-octubre, solo 4° medio) y Periodo 3 (octubre, todos excepto 4° medio).',
    },
    {
      categoria: 'tramite',
      pregunta: '¿Nosotros elegimos en qué colegio rinde el examen?',
      respuesta:
        'No — la entidad examinadora la asigna automáticamente el Mineduc según disponibilidad de cupos e infraestructura de la región. Hay que contactar a ese establecimiento 10 días antes del examen para confirmar fecha y hora.',
    },
    {
      categoria: 'tramite',
      pregunta: '¿Qué pasa si mi hijo/a reprueba?',
      respuesta:
        'No hay segunda oportunidad dentro del mismo periodo. Solo se puede volver a inscribir en otro periodo disponible, si hay cupos — por eso es tan importante llegar con una preparación real, no solo "haber visto" la materia.',
    },
    {
      categoria: 'tramite',
      pregunta: '¿El trámite de inscripción al examen tiene costo?',
      respuesta:
        'No, el trámite de inscripción ante el Mineduc es completamente gratuito. Lo debe realizar el padre, madre o tutor legal, no el menor directamente.',
    },
  ];

  toggle(i: number) {
    this.abierta.set(this.abierta() === i ? null : i);
  }
}
