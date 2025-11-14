# Flask BigData - Docker Setup

Configuración Docker para ejecutar la aplicación Flask con uvicorn y nginx como proxy reverso.

## Estructura del Proyecto

```
flask-bigdata-2526/
├── app.py                 # Aplicación Flask
├── Dockerfile            # Imagen de la aplicación
├── docker-compose.yml    # Orquestación de servicios
├── requirements.txt      # Dependencias Python
├── nginx/
│   └── nginx.conf       # Configuración nginx
├── templates/           # Templates HTML
└── .dockerignore        # Archivos excluidos en Docker
```

## Servicios

- **flask-app**: Aplicación Flask ejecutándose con uvicorn (puerto 8000)
- **nginx**: Proxy reverso (puertos 80, 443)
- **mongodb**: Base de datos MongoDB (puerto 27017) - Solo perfil `dev`
- **redis**: Cache Redis (puerto 6379) - Solo perfil `dev`

## Comandos de Uso

### Ejecutar en Producción
```bash
# Construir y ejecutar servicios principales
docker-compose up -d flask-app nginx

# Ver logs
docker-compose logs -f flask-app
docker-compose logs -f nginx
```

### Ejecutar en Desarrollo
```bash
# Con servicios adicionales (MongoDB, Redis)
docker-compose --profile dev up -d

# O todos los servicios
docker-compose --profile dev up -d --build
```

### Comandos de Gestión
```bash
# Detener servicios
docker-compose down

# Reconstruir imagen
docker-compose build flask-app

# Acceder al contenedor
docker-compose exec flask-app bash

# Limpiar volúmenes
docker-compose down -v
```

## Variables de Entorno

Las siguientes variables pueden configurarse:

- `FLASK_ENV`: Entorno de Flask (development/production)
- `MONGODB_URL`: URL de conexión a MongoDB
- `MONGODB_DB`: Nombre de la base de datos
- `MAX_CONTENT_LENGTH`: Tamaño máximo de archivos subidos

## Configuración de Seguridad

- Usuario no-root en contenedor Flask
- Headers de seguridad en nginx
- Health checks configurados
- Red aislada entre contenedores
- Timeouts y buffers configurados

## Puertos Expuestos

- `80`: HTTP via nginx
- `443`: HTTPS via nginx
- `8000`: Aplicación Flask directa
- `27017`: MongoDB (solo dev)
- `6379`: Redis (solo dev)

## Notas de Seguridad

⚠️ **IMPORTANTE**: Antes de usar en producción:

1. Configurar autenticación MongoDB
2. Implementar validación de archivos
3. Añadir sistema de autenticación
4. Configurar HTTPS con certificados SSL
5. Configurar variables de entorno seguras
6. Revisar el informe de vulnerabilidades incluido

Ver `informe_vulnerabilidades.md` para detalles completos.