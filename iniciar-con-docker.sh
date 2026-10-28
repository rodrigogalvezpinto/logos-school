#!/bin/bash

# Script de inicio para Logos School con Docker
# Este script levanta PostgreSQL, aplica migraciones, importa contenido e inicia backend y frontend

set -e

echo "🚀 Iniciando Logos School con Docker..."

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker Desktop primero."
    exit 1
fi

# Levantar PostgreSQL
echo "📦 Levantando PostgreSQL con Docker Compose..."
docker-compose up -d postgres

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
until docker exec logos-postgres pg_isready -U logos_dev > /dev/null 2>&1; do
    echo "  - PostgreSQL no está listo aún, esperando..."
    sleep 2
done
echo "✅ PostgreSQL está listo"

# Ir al backend
cd backend

# Verificar si .env existe, si no, copiar del ejemplo
if [ ! -f .env ]; then
    echo "📝 Creando .env desde .env.example..."
    cp ../.env.example .env
    echo "⚠️  Por favor revisa .env y ajusta las variables si es necesario"
fi

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "⚠️  No se encontró .venv. Creando entorno virtual..."
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
fi

# Aplicar migraciones
echo "🔄 Aplicando migraciones de Alembic..."
uv run alembic upgrade head

# Importar contenido (si existe el script)
if [ -f "scripts/importar_contenido.py" ]; then
    echo "📚 Importando contenido de los cursos..."
    uv run python scripts/importar_contenido.py
fi

# Importar planes (si existe el script)
if [ -f "scripts/sembrar_planes.py" ]; then
    echo "📋 Sembrando planes de estudio..."
    uv run python scripts/sembrar_planes.py
fi

# Crear datos de prueba (si existe el script)
if [ -f "scripts/datos_de_prueba.py" ]; then
    echo "👤 Creando datos de prueba..."
    uv run python scripts/datos_de_prueba.py
fi

# Iniciar backend en background
echo "🔧 Iniciando backend en background (puerto 8000)..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Volver al directorio raíz
cd ..

# Iniciar frontend en background
echo "🎨 Iniciando frontend en background (puerto 4200)..."
cd frontend
npm start &
FRONTEND_PID=$!

# Volver al directorio raíz
cd ..

echo ""
echo "✅ Logos School está iniciado!"
echo ""
echo "📊 Servicios corriendo:"
echo "  - PostgreSQL: localhost:5432"
echo "  - Backend: http://localhost:8000"
echo "  - Frontend: http://localhost:4200"
echo ""
echo "👤 Credenciales de prueba:"
echo "  - Apoderado: apoderado.prueba@logos.cl / Logos2026!"
echo "  - Profesor: profesor.prueba@logos.cl / Logos2026!"
echo "  - Admin: admin.prueba@logos.cl / Logos2026!"
echo ""
echo "⏹️  Para detener los servicios:"
echo "  - Presiona Ctrl+C en esta terminal"
echo "  - O ejecuta: docker-compose down"
echo ""
echo "💡 Para detener solo PostgreSQL: docker-compose stop postgres"
echo ""

# Esperar a que el usuario presione Ctrl+C
trap "echo ''; echo '🛑 Deteniendo servicios...'; kill $BACKEND_PID 2>/dev/null || true; kill $FRONTEND_PID 2>/dev/null || true; docker-compose stop postgres; echo '✅ Servicios detenidos'; exit 0" INT TERM

wait
