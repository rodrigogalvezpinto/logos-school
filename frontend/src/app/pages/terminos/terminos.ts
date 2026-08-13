import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

@Component({
  selector: 'app-terminos',
  standalone: true,
  imports: [RouterLink, Logo],
  template: `
    <div class="pagina">
      <header class="landing__nav">
        <a routerLink="/"><app-logo /></a>
        <a routerLink="/" class="btn btn--secundario">Volver al inicio</a>
      </header>

      <h1>Términos y Condiciones</h1>
      <p class="fecha">Última actualización: agosto de 2026</p>

      <section>
        <h2>Qué es Logos School</h2>
        <p>Logos School es una plataforma de apoyo de estudio para niños, niñas y adolescentes que se
        preparan para rendir los Exámenes Libres de Validación de Estudios del Ministerio de
        Educación de Chile. No somos un colegio ni una institución reconocida por el Mineduc — el
        trámite de inscripción al examen real lo realiza siempre el apoderado directamente con el
        Estado.</p>
      </section>

      <section>
        <h2>Quién puede registrarse</h2>
        <p>El registro lo debe hacer un adulto responsable (apoderado, tutor u otro adulto que
        matricule al menor), quien agrega los perfiles de los alumnos bajo su cuenta.</p>
      </section>

      <section>
        <h2>Planes y pagos</h2>
        <p>Logos School ofrece planes de pago (mensual, por periodo de examinación, o anual). Los montos
        vigentes se muestran siempre antes de confirmar cualquier pago. El acceso al contenido
        contratado se mantiene mientras el plan esté activo.</p>
      </section>

      <section>
        <h2>Contenido y precisión</h2>
        <p>El contenido de estudio está basado fielmente en los temarios oficiales del Mineduc/UCE,
        pero es de elaboración propia — no reproduce preguntas reales del examen oficial. Logos School no
        garantiza la aprobación del examen real; el resultado depende del estudio y preparación del
        alumno.</p>
      </section>

      <section>
        <h2>Contacto</h2>
        <p>Para consultas sobre estos términos, escríbenos a través de los canales de contacto
        publicados en la plataforma.</p>
      </section>
    </div>
  `,
  styles: [
    `
      .pagina {
        max-width: 720px;
        margin: 0 auto;
        padding: 0 2rem 4rem;
      }
      .landing__nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0 2.5rem;
      }
      h1 {
        font-size: 1.8rem;
        margin-bottom: 0.25rem;
      }
      .fecha {
        color: var(--texto-secundario);
        font-size: 0.85rem;
        margin-bottom: 2rem;
      }
      section {
        margin-bottom: 1.75rem;
      }
      h2 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
      }
      p {
        color: var(--texto-secundario);
        line-height: 1.6;
      }
    `,
  ],
})
export class Terminos {}
