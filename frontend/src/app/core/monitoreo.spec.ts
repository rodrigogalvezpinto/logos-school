import { describe, expect, it } from 'vitest';
import { limpiarEvento } from './monitoreo';

describe('limpiarEvento (Sentry sin datos personales)', () => {
  it('quita parámetros de URL, usuario, migas y encabezados', () => {
    const e = limpiarEvento({
      type: undefined,
      request: { url: 'https://logos.cl/restablecer?token=secreto', query_string: 'token=secreto', headers: { a: 'b' }, cookies: { c: 'd' } },
      user: { email: 'mama@x.cl' },
      breadcrumbs: [{ message: 'Sofía Pérez' }],
      message: 'falló',
    } as never) as Record<string, any>;
    expect(e['request'].url).toBe('https://logos.cl/restablecer');
    expect(e['request'].query_string).toBeUndefined();
    expect(e['request'].headers).toBeUndefined();
    expect(e['user']).toBeUndefined();
    expect(e['breadcrumbs']).toBeUndefined();
    expect(e['message']).toBe('falló');
  });
});
