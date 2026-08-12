import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-estudiar-oa',
  standalone: true,
  imports: [RouterLink],
  template: `
    <a routerLink="/alumno/asignaturas/matematica" class="volver">← Volver a Matemática</a>
    <span class="etiqueta">OA 1 · Números y Operaciones</span>
    <h1>Representar y describir números hasta el 10.000</h1>
    <p class="lead">
      Vas a leer, escribir, comparar, ordenar, componer y descomponer números hasta 10.000,
      entendiendo el <strong>valor posicional</strong> de cada dígito: unidad (U), decena (D),
      centena (C), unidad de mil (UM) y decena de mil (DM).
    </p>

    <div class="tarjeta bloque">
      <h3>¿Por qué importa?</h3>
      <p>
        Entender el valor posicional es la base de todas las operaciones que vienen después:
        sumar, restar, multiplicar y dividir números grandes solo funciona bien si sabes qué
        "vale" cada dígito según su posición.
      </p>
    </div>

    <h3>Ejemplo resuelto</h3>
    <div class="tarjeta bloque bloque--ejemplo">
      <p><strong>Descomponer un número según su valor posicional</strong></p>
      <p>El número <strong>7.352</strong> se puede descomponer así:</p>
      <ul>
        <li>7 está en la posición de las <strong>unidades de mil</strong> → vale 7.000</li>
        <li>3 está en la posición de las <strong>centenas</strong> → vale 300</li>
        <li>5 está en la posición de las <strong>decenas</strong> → vale 50</li>
        <li>2 está en la posición de las <strong>unidades</strong> → vale 2</li>
      </ul>
      <p>Entonces: 7.352 = 7.000 + 300 + 50 + 2</p>
    </div>

    <a routerLink="/alumno/autoevaluacion/oa1" class="btn btn--primario btn--grande">Practicar este tema</a>
  `,
  styles: [
    `
      .volver {
        display: inline-block;
        color: var(--texto-secundario);
        text-decoration: none;
        margin-bottom: 1.25rem;
        font-size: 0.9rem;
      }
      .etiqueta {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--color-primario);
        text-transform: uppercase;
      }
      h1 {
        margin: 0.4rem 0 1rem;
        font-size: 1.6rem;
      }
      .lead {
        font-size: 1.05rem;
        color: var(--texto-secundario);
        max-width: 640px;
        margin-bottom: 1.75rem;
      }
      .bloque {
        margin-bottom: 1.5rem;
        max-width: 640px;
      }
      .bloque--ejemplo {
        background: var(--color-primario-suave);
        border-left: 4px solid var(--color-primario);
      }
    `,
  ],
})
export class EstudiarOa {
  @Input() oaId = '';
}
