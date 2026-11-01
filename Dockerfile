# ---------- مرحله ۱: ساخت CSS (Tailwind) و جزیره‌ی React ----------
FROM node:20-alpine AS assets
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
COPY backend/ /build/backend/
RUN npm run build

# ---------- مرحله ۲: اپ جنگو ----------
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=120 --retries=10 -r requirements.txt
COPY backend/ .
COPY --from=assets /build/backend/static/site ./static/site
RUN useradd -m app && chown -R app /app
USER app
RUN DJANGO_DEBUG=true python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile -"]
