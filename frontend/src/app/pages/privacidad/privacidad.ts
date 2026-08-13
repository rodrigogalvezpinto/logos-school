import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

@Component({
  selector: 'app-privacidad',
  standalone: true,
  imports: [RouterLink, Logo],
  template: `
    <div class="pagina">
      <header class="landing__nav">
        <a routerLink="/"><app-logo /></a>
        <a routerLink="/" class="btn btn--secundario">Volver al inicio</a>
      </header>

      <main>
      <h1>Política de Privacidad</h1>
      <p class="fecha">Última actualización: agosto de 2026</p>

      <section>
        <h2>Qué datos recolectamos</h2>
        <p>Del Apoderado: nombre, correo electrónico y contraseña (encriptada). Del Alumno: nombre,
        apellidos, fecha de nacimiento, RUT y curso. No pedimos domicilio exacto, datos de salud ni
        otros datos sensibles.</p>
      </section>

      <section>
        <h2>Para qué los usamos</h2>
        <p>Exclusivamente para operar la plataforma: crear tu cuenta, mostrar el contenido de estudio
        correspondiente al curso de tu hijo o hija, y guardar su progreso y notas. Nunca usamos estos
        datos con fines publicitarios ni los vendemos a terceros.</p>
      </section>

      <section>
        <h2>Tus derechos</h2>
        <p>Puedes solicitar en cualquier momento ver, corregir o eliminar los datos de cualquier Alumno
        vinculado a tu cuenta, escribiendo a nuestro correo de contacto.</p>
      </section>
      <section>
        <h2>Marco legal</h2>
        <p>Esta plataforma trata los datos conforme a la Ley 21.719 de Protección de Datos Personales
        de Chile. Para más detalle sobre nuestro enfoque de privacidad de menores, consulta nuestro
        documento de planificación interno (disponible bajo solicitud).</p>
      </section>
      </main>
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
export class Privacidad {}
