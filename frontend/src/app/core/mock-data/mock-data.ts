export interface AsignaturaMock {
  id: string;
  nombre: string;
  icono: string;
  color: string;
  avance: number; // 0-100
  objetivos: ObjetivoMock[];
}

export interface ObjetivoMock {
  id: string;
  codigo: string;
  titulo: string;
  estado: 'no_iniciado' | 'en_progreso' | 'dominado';
  resumen: string;
}

export interface PreguntaMock {
  id: string;
  enunciado: string;
  tipo: 'alternativas' | 'verdadero_falso';
  opciones?: string[];
}

export const ASIGNATURAS_4_BASICO: AsignaturaMock[] = [
  {
    id: 'lenguaje',
    nombre: 'Lenguaje y Comunicación',
    icono: 'libro',
    color: '#5B4FE9',
    avance: 62,
    objetivos: [
      {
        id: 'oa4',
        codigo: 'OA 4',
        titulo: 'Comprender narraciones',
        estado: 'dominado',
        resumen:
          'Leer cuentos y otras narraciones, identificando personajes, lugar, tiempo y las acciones principales.',
      },
      {
        id: 'oa5',
        codigo: 'OA 5',
        titulo: 'Comprender poemas',
        estado: 'en_progreso',
        resumen: 'Reconocer el lenguaje figurado y el efecto que producen los poemas en quien los lee.',
      },
      {
        id: 'oa6',
        codigo: 'OA 6',
        titulo: 'Textos informativos',
        estado: 'no_iniciado',
        resumen: 'Leer noticias, biografías e instrucciones para aprender sobre el mundo.',
      },
    ],
  },
  {
    id: 'matematica',
    nombre: 'Matemática',
    icono: 'regla',
    color: '#FF6B4A',
    avance: 40,
    objetivos: [
      {
        id: 'oa1',
        codigo: 'OA 1',
        titulo: 'Números hasta 10.000',
        estado: 'dominado',
        resumen: 'Representar, describir, comparar y ordenar números hasta el 10.000.',
      },
      {
        id: 'oa2',
        codigo: 'OA 2',
        titulo: 'Adición y sustracción',
        estado: 'en_progreso',
        resumen: 'Resolver problemas de suma y resta con números hasta 10.000.',
      },
    ],
  },
  {
    id: 'ciencias',
    nombre: 'Ciencias Naturales',
    icono: 'hoja',
    color: '#22C55E',
    avance: 25,
    objetivos: [
      {
        id: 'oa-cn1',
        codigo: 'OA 1',
        titulo: 'Ciclo del agua',
        estado: 'en_progreso',
        resumen: 'Describir el ciclo del agua y su importancia para los seres vivos.',
      },
    ],
  },
  {
    id: 'historia',
    nombre: 'Historia, Geografía y Cs. Sociales',
    icono: 'mapa',
    color: '#F59E0B',
    avance: 10,
    objetivos: [
      {
        id: 'oa-hi1',
        codigo: 'OA 1',
        titulo: 'Pueblos originarios',
        estado: 'no_iniciado',
        resumen: 'Ubicar y caracterizar los pueblos indígenas que habitaban el territorio chileno.',
      },
    ],
  },
];

export const PREGUNTAS_MOCK: PreguntaMock[] = [
  {
    id: 'p1',
    tipo: 'alternativas',
    enunciado: '¿Cuál es el valor posicional del dígito 7 en el número 7.352?',
    opciones: ['Unidad', 'Decena', 'Centena', 'Unidad de mil'],
  },
  {
    id: 'p2',
    tipo: 'verdadero_falso',
    enunciado: 'En el número 3.084, el dígito 8 representa 8 decenas.',
  },
  {
    id: 'p3',
    tipo: 'alternativas',
    enunciado: '¿Cuál de los siguientes números es mayor?',
    opciones: ['6.482', '6.824', '6.248', '6.284'],
  },
];
