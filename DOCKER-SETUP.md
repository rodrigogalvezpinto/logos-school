# Configuración con Docker para Logos School

Este documento explica cómo usar Docker para tener PostgreSQL local y poder mover el proyecto entre PCs fácilmente.

## 🚀 Inicio rápido

Solo necesitas Docker Desktop instalado, luego ejecuta:

```bash
./iniciar-con-docker.sh
```

Este script:
1. Levanta PostgreSQL en Docker
2. Aplica migraciones de la base de datos
3. Importa contenido de los cursos
4. Crea datos de prueba
5. Inicia backend (puerto 8000)
6. Inicia frontend (puerto 4200)

## 📦 Servicios Docker

### PostgreSQL
- **Imagen:** postgres:16-alpine
- **Puerto:** 5432
- **Usuario:** logos_dev
- **Contraseña:** logos_dev_local
- **Base de datos:** logos_dev
- **Persistencia:** Volumen Docker `postgres_data` (los datos persisten aunque detengas el contenedor)

## 🔧 Configuración

### Archivos creados

1. **docker-compose.yml** - Configuración de PostgreSQL
2. **.env.example** - Plantilla de variables de entorno
3. **iniciar-con-docker.sh** - Script de inicio automatizado

### Variables de entorno

El backend usa `.env` (no está en el repositorio por seguridad). Para crearlo:

```bash
cp .env.example backend/.env
```

Las variables principales:
- `DATABASE_URL` - Conexión a PostgreSQL
- `JWT_SECRET` - Clave para tokens JWT
- `JWT_EXPIRACION_MINUTOS` - Tiempo de expiración de tokens

## 🔄 Mover a otro PC

En el otro PC:

1. Clonar el repositorio:
   ```bash
   git clone <tu-repo>
   cd Logos
   ```

2. Instalar Docker Desktop

3. Instalar Python 3.12+ y Node.js

4. Ejecutar:
   ```bash
   ./iniciar-con-docker.sh
   ```

¡Listo! Todo funcionará sin configuración adicional.

## 💾 Persistencia de datos

Los datos de PostgreSQL persisten en el volumen Docker `postgres_data`. Si borras el contenedor, los datos no se pierden.

Para limpiar completamente los datos:
```bash
docker-compose down -v
```

## 🛑 Comandos útiles

```bash
# Iniciar solo PostgreSQL
docker-compose up -d postgres

# Ver logs de PostgreSQL
docker-compose logs -f postgres

# Detener PostgreSQL
docker-compose stop postgres

# Eliminar contenedor y volumen (limpieza completa)
docker-compose down -v

# Entrar a PostgreSQL directamente
docker exec -it logos-postgres psql -U logos_dev logos_dev
```

## ⚠️ Notas importantes

- Docker Desktop debe estar corriendo antes de ejecutar el script
- El puerto 5432 debe estar disponible en tu sistema
- Los servicios externos (Google OAuth, Resend, etc.) son opcionales para desarrollo
- Para producción, usa Neon/Render/Cloudflare Pages según `planificacion/17-infraestructura-y-entornos.md`
