# Beauty Salon Website + Online Appointment Booking

Django (HTML Templates) + Tailwind | React only for the booking page | PostgreSQL | Docker

## Project Structure

- `backend/templates/` – HTML pages styled with Tailwind. Most of the UI and visual design work happens here.
- `backend/web/` – Views, login/registration forms, and Jalali date filtering.
- `backend/booking/` – Booking models and API.
- `frontend/src/` – Tailwind styles (`styles.css`) and the only React component (`Booking.jsx`).

The frontend build generates two files: `style.css` (used across all pages) and `islands.js` (used only on `/book/`).

## Running with Docker

```bash
cp .env.example .env        # Change SECRET_KEY and database password
docker compose up -d --build --remove-orphans
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py seed_demo   # Sample services (optional)
```

Website: http://localhost  
Admin panel: http://localhost/admin/

## Local Development Without Docker

```bash
cd frontend && npm install && npm run watch        # Terminal 1: Automatic CSS/JS build

cd backend && pip install -r requirements.txt

export DJANGO_DEBUG=true && python manage.py migrate && python manage.py runserver   # Terminal 2
```

## Production Deployment (HTTPS)

Change the port mapping in `docker-compose.yml` to `127.0.0.1:8000:8000` and put Caddy in front of it:

```caddy
yourdomain.com {
    reverse_proxy localhost:8000
}
```

In `.env`, configure:

```env
DJANGO_HTTPS=true
DJANGO_ALLOWED_HOSTS=yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com
DRF_NUM_PROXIES=1
DJANGO_HSTS_SECONDS=31536000
```

Set `DJANGO_HSTS_SECONDS` after verifying that HTTPS is working correctly.

## Security

- Session-based authentication with HttpOnly/Secure cookies.
- CSRF protection on all forms and API endpoints.
- Strict Content Security Policy (CSP), with no inline scripts/styles or external CDNs. Fonts are self-hosted.
- Rate limiting for login, registration, and booking attempts.
- Users can only view and cancel their own appointments.
- Database `UniqueConstraint` prevents duplicate bookings for the same time slot.
- Containers run as a non-root user.

## Future Improvements

- Redis for rate limiting.
- SMS appointment reminders.
- Support for multiple service providers and staff members.
- Portfolio gallery with image uploads.
- Database backups.