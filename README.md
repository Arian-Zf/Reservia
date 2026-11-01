# سایت سالن زیبایی + رزرو آنلاین نوبت

Django (قالب‌های HTML) + Tailwind | React فقط برای صفحه‌ی رزرو | Postgres | Docker

## ساختار
- `backend/templates/` صفحه‌های HTML (با Tailwind) — بیشتر کار ظاهری اینجاست
- `backend/web/` ویوها، فرم ورود/ثبت‌نام، فیلتر تاریخ شمسی
- `backend/booking/` مدل‌ها و API رزرو
- `frontend/src/` استایل Tailwind (`styles.css`) و تنها کد React (`Booking.jsx`)

بیلد فرانت دو فایل می‌سازد: `style.css` (همه‌ی صفحه‌ها) و `islands.js` (فقط /book/).

## اجرا با Docker
```bash
cp .env.example .env        # SECRET_KEY و رمز دیتابیس را عوض کنید
docker compose up -d --build --remove-orphans
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py seed_demo   # خدمات نمونه (اختیاری)
```
سایت: http://localhost — ادمین: http://localhost/admin/

## توسعه‌ی لوکال بدون Docker
```bash
cd frontend && npm install && npm run watch        # ترمینال ۱: بیلد خودکار CSS/JS
cd backend && pip install -r requirements.txt
export DJANGO_DEBUG=true && python manage.py migrate && python manage.py runserver   # ترمینال ۲
```

## پروداکشن (HTTPS)
پورت را در docker-compose به `127.0.0.1:8000:8000` تغییر دهید و جلوی آن Caddy بگذارید:
```
yourdomain.com {
    reverse_proxy localhost:8000
}
```
در `.env`: `DJANGO_HTTPS=true`، `DJANGO_ALLOWED_HOSTS`، `DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com`،
`DRF_NUM_PROXIES=1` و بعد از اطمینان `DJANGO_HSTS_SECONDS=31536000`.

## امنیت
- ورود با session و کوکی HttpOnly/Secure؛ CSRF روی همه‌ی فرم‌ها و API
- CSP سخت‌گیرانه (بدون inline script/style و بدون CDN بیرونی؛ فونت هم self-host)
- محدودیت تعداد تلاش برای ورود/ثبت‌نام و رزرو
- هر کاربر فقط نوبت‌های خودش را می‌بیند/لغو می‌کند
- جلوگیری از رزرو دوباره‌ی یک زمان با UniqueConstraint دیتابیس
- کانتینر با کاربر غیر root

## قدم‌های بعدی
Redis برای rate limit، پیامک یادآوری، چند ارائه‌دهنده/پرسنل، گالری نمونه‌کار (آپلود عکس)، بکاپ دیتابیس.
