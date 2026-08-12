import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-evaluaciones',
  standalone: true,
  imports: [RouterLink],
  template: `
    <h1>Pruebas y Exámenes</h1>
    <p class="subtitulo">Todo lo que puedes rendir, agrupado por asignatura.</p>

    <div class="grupo">
      <h2>Matemática</h2>
      <div class="fila tarjeta">
        <div>
          <h3>Números y Operaciones</h3>
          <p>Prueba de unidad · sin tiempo límite</p>
        </div>
        <a routerLink="/alumno/prueba/matematica-num" class="btn btn--primario">Rendir</a>
      </div>
      <div class="fila tarjeta">
        <div>
          <h3>Patrones y Álgebra</h3>
          <p>Prueba de unidad · sin tiempo límite</p>
        </div>
        <a routerLink="/alumno/prueba/matematica-alg" class="btn btn--secundario">Rendir</a>
      </div>
    </div>

    <div class="grupo">
      <h2>Examen simulacro</h2>
      <div class="fila fila--examen tarjeta">
        <div>
          <h3>Examen integrado Forma A</h3>
          <p>20 preguntas · 90 minutos · imita el examen real</p>
        </div>
        <a routerLink="/examen/integrado-a" class="btn btn--primario">Comenzar examen</a>
      </div>
    </div>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grupo {
        margin-bottom: 2rem;
      }
      .grupo h2 {
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
      }
      .fila {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;

        h3 {
          margin: 0 0 0.2rem;
          font-size: 1rem;
        }
        p {
          margin: 0;
          color: var(--texto-secundario);
          font-size: 0.85rem;
        }
      }
      .fila--examen {
        border: 1.5px solid var(--color-primario);
      }
    `,
  ],
})
export class Evaluaciones {}
