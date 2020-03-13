## Desarrollo

### Instalación

    docker-compose up -d --build backend_dev
    
### Ejecución

    docker-compose up -d backend_dev
    
## Producción

### Instalación

    docker-compose up -d --build backend
    
## Ejecución

    docker-compose up -d backend
    
    
## Utilidades


Ver logs de contenedor

    docker-compose logs -f backend
    docker-compose logs -f postgres
    
Ejecutar Shell de Django:

    docker-compose exec backend python manage.py shell
    
Migraciones:

    docker-compose exec backend python manage.py makemigrations
    docker-compose exec backend python manage.py migrate