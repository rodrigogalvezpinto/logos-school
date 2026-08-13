/** Validación de RUT chileno (módulo 11) — misma lógica que backend/app/core/rut.py,
 * para dar feedback inmediato en el formulario sin esperar la respuesta del servidor. */
export function validarRut(rutCompleto: string): boolean {
  const limpio = rutCompleto.replace(/[.\-\s]/g, '').toUpperCase();
  if (limpio.length < 2) return false;
  const cuerpo = limpio.slice(0, -1);
  const dv = limpio.slice(-1);
  if (!/^\d+$/.test(cuerpo)) return false;

  let suma = 0;
  let multiplicador = 2;
  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo[i], 10) * multiplicador;
    multiplicador = multiplicador < 7 ? multiplicador + 1 : 2;
  }
  const resto = 11 - (suma % 11);
  const dvEsperado = resto === 11 ? '0' : resto === 10 ? 'K' : String(resto);
  return dvEsperado === dv;
}
