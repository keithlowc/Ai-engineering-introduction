# Property Owner CRM

A Django-based Customer Relationship Management (CRM) system for managing store property owners information and ratings.

## Features

- **Property Owner Management**: Add, edit, delete, and view property owner details
- **Rating System**: Rate owners on reliability, communication, maintenance, and overall performance
- **Interaction Logging**: Track all interactions (calls, emails, meetings) with property owners
- **Search & Filter**: Search by name, email, company, or filter by rating and status
- **Dashboard**: Quick overview of key metrics and recent interactions
- **Responsive Design**: Bootstrap-based responsive UI

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
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

7. Access the application:
   - Dashboard: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Usage

### Dashboard
The main dashboard provides quick stats about property owners and recent interactions.

### Managing Owners
- Click "+ New Owner" to add a new property owner
- Use the search bar to find owners by name, email, or company
- Filter by rating and status
- View detailed owner information including rating history

### Rating System
Property owners can be rated on:
- **Reliability**: How dependable and punctual they are
- **Communication**: Responsiveness and clarity of communication
- **Maintenance**: Property maintenance standards
- **Overall**: Overall rating based on your experience

### Interaction Tracking
Log interactions with owners including:
- Phone calls
- Emails
- In-person meetings
- Text messages
- Other interactions

## Models

### PropertyOwner
- Basic contact information
- Rating fields (1-5 scale)
- Notes and status
- Timestamps

### InteractionLog
- Links to PropertyOwner
- Interaction type
- Subject and notes
- Date/time tracking

## Admin Interface

Access the Django admin interface at `/admin/` to manage owners and interactions with full CRUD capabilities.

## Technologies Used

- Django 4.2
- SQLite (default)
- Bootstrap 5
- HTML5/CSS3

## License

MIT
