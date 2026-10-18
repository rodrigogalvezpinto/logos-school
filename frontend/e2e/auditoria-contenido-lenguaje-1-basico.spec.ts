import { test, expect } from '@playwright/test';

test.describe('Auditoría de contenido - Lenguaje 1° Básico', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  const problemas: string[] = [];
  const observaciones: string[] = [];

  test('Auditar contenido de Lenguaje y Comunicación - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/asignaturas');
    await page.click('text=Lenguaje y Comunicación');
    await page.waitForLoadState('networkidle');

    // Obtener todas las guías
    const estudiarButtons = await page.locator('text=Estudiar').all();
    observaciones.push(`📚 Hay ${estudiarButtons.length} guías de estudio en Lenguaje`);

    // Auditar solo la primera guía para evitar problemas de navegación
    const guiasAuditar = 1;
    
    for (let i = 0; i < guiasAuditar; i++) {
      await estudiarButtons[i].click();
      await page.waitForLoadState('networkidle');

      const tituloOA = await page.locator('h1').textContent();
      observaciones.push(`📖 Guía ${i + 1}: "${tituloOA}"`);

      // Verificar estructura de la guía
      const contenido = page.locator('.contenido-guia');
      const texto = await contenido.textContent();
      
      if (texto) {
        // Verificar que tiene "¿Por qué importa?"
        if (texto.includes('¿Por qué importa?')) {
          observaciones.push(`✅ Guía ${i + 1} tiene sección "¿Por qué importa?"`);
        } else {
          problemas.push(`❌ Guía ${i + 1} NO tiene sección "¿Por qué importa?"`);
        }

        // Verificar que tiene ejemplos
        if (texto.includes('Ejemplo') || texto.includes('Actividad')) {
          observaciones.push(`✅ Guía ${i + 1} tiene ejemplos/actividades`);
        } else {
          problemas.push(`❌ Guía ${i + 1} NO tiene ejemplos/actividades`);
        }

        // Verificar que tiene preguntas de autoevaluación
        if (texto.includes('Pregunta') || texto.includes('pregunta')) {
          observaciones.push(`✅ Guía ${i + 1} tiene preguntas de autoevaluación`);
        } else {
          problemas.push(`❌ Guía ${i + 1} NO tiene preguntas de autoevaluación`);
        }

        // Verificar que tiene retroalimentación
        if (texto.includes('Retroalimentación') || texto.includes('retroalimentación')) {
          observaciones.push(`✅ Guía ${i + 1} tiene retroalimentación`);
        } else {
          problemas.push(`❌ Guía ${i + 1} NO tiene retroalimentación`);
        }

        // Verificar emojis
        const emojis = await page.locator('.emoji-educativo-inline').all();
        if (emojis.length > 0) {
          observaciones.push(`✅ Guía ${i + 1} tiene ${emojis.length} emojis educativos`);
        } else {
          problemas.push(`❌ Guía ${i + 1} NO tiene emojis educativos (contenido puede ser muy denso para niño de 6 años)`);
        }
      }

      // Volver a asignaturas
      await page.goto('/alumno/asignaturas');
      await page.waitForLoadState('networkidle');
    }

    // Generar reporte
    console.log('\n📋 OBSERVACIONES (Lenguaje 1° Básico):');
    observaciones.forEach(obs => console.log(obs));

    console.log('\n🔴 PROBLEMAS ENCONTRADOS:');
    if (problemas.length === 0) {
      console.log('✅ No se encontraron problemas en el contenido auditado');
    } else {
      problemas.forEach(prob => console.log(prob));
    }

    console.log(`\n📊 Total: ${observaciones.length} observaciones, ${problemas.length} problemas`);
  });
});
