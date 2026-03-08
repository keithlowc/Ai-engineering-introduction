# Property CRM - Django Application

A Django-based Customer Relationship Management (CRM) system for managing property owners and their properties, including ratings and reviews.

## Features

- **Property Owner Management**: Store and manage property owner information
- **Property Management**: Track properties owned by each owner
- **Rating System**: Rate and review properties
- **Contact Tracking**: Track contact status and communication history
- **User Assignment**: Assign property owners to team members
- **RESTful API**: Full API for all operations
- **PostgreSQL Database**: Robust database backend
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)

## Setup

### Using Docker Compose

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Copy and configure environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your configuration (especially `SECRET_KEY` and `DB_PASSWORD`)

4. Build and run with Docker Compose:
```bash
docker-compose up -d
```

5. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

6. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

7. Access the application:
   - Admin: http://localhost:8000/admin
   - API: http://localhost:8000/api/

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Property Owners
- `GET /api/owners/` - List all property owners
- `POST /api/owners/` - Create a new property owner
- `GET /api/owners/{id}/` - Retrieve a specific owner
- `PUT /api/owners/{id}/` - Update a property owner
- `DELETE /api/owners/{id}/` - Delete a property owner
- `POST /api/owners/{id}/assign/` - Assign owner to a user
- `POST /api/owners/{id}/change_status/` - Change contact status

### Properties
- `GET /api/properties/` - List all properties
- `POST /api/properties/` - Create a new property
- `GET /api/properties/{id}/` - Retrieve a specific property
- `PUT /api/properties/{id}/` - Update a property
- `DELETE /api/properties/{id}/` - Delete a property
- `GET /api/properties/{id}/average_rating/` - Get average property rating

### Ratings
- `GET /api/ratings/` - List all ratings
- `POST /api/ratings/` - Create a new rating
- `GET /api/ratings/{id}/` - Retrieve a specific rating
- `PUT /api/ratings/{id}/` - Update a rating
- `DELETE /api/ratings/{id}/` - Delete a rating

## Database Schema

### PropertyOwner
- Basic contact information (name, email, phone)
- Company information
- Address details
- Contact status tracking
- Rating system
- Assignment to team members

### Property
- Owner reference
- Property type (residential, commercial, industrial, land)
- Location details
- Property specifications (bedrooms, bathrooms, square footage)
- Year built and estimated value

### PropertyRating
- Property reference
- Rating (1-5 stars)
- Comments
- Reviewer tracking

## Environment Variables

See `.env.example` for all available configuration options. Key variables:

- `DEBUG` - Django debug mode
- `SECRET_KEY` - Django secret key (change in production)
- `DB_*` - Database configuration
- `ALLOWED_HOSTS` - Allowed host domains
- `EMAIL_*` - Email configuration

## Security Notes

⚠️ **Important**: Never commit `.env` files or hardcoded secrets to version control.

- Store all secrets in environment variables
- Use strong `SECRET_KEY` in production
- Rotate database passwords regularly
- Enable HTTPS in production
- Use `python-decouple` for environment variable management

## Development

### Running Tests
```bash
python manage.py test
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Generate a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` appropriately
4. Use a production database (PostgreSQL)
5. Set up proper email configuration
6. Enable HTTPS/SSL
7. Use a production WSGI server (Gunicorn, uWSGI)
8. Set up proper logging and monitoring

## License

MIT License
