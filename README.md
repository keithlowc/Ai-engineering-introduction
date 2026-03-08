# Django Docker Compose PostgreSQL Setup

This is a Django application migrated to use Docker Compose with PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Installation & Setup

1. Clone the repository

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up -d --build
```

This will:
- Build the Django application image
- Start PostgreSQL database
- Run migrations automatically
- Start the Django development server

4. Access the application:
- Django app: http://localhost:8000
- Django admin: http://localhost:8000/admin

## Available Commands

### Start containers
```bash
docker-compose up
```

### Start in detached mode
```bash
docker-compose up -d
```

### Stop containers
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f web
docker-compose logs -f db
```

### Run Django management commands
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Access database
```bash
docker-compose exec db psql -U postgres -d django_db
```

## Environment Variables

Edit `.env` file to customize:
- `DEBUG` - Django debug mode
- `SECRET_KEY` - Django secret key
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example
├── .dockerignore
└── README.md
```

## Notes

- The database data is persisted in a Docker volume `postgres_data`
- Migrations run automatically on container startup
- For production, update `DEBUG=False` and set a strong `SECRET_KEY` in `.env`