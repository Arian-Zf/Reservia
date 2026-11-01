from django.conf import settings
from django.core.cache import cache


def client_ip(request):
    n = settings.REST_FRAMEWORK.get("NUM_PROXIES", 0)
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if n and xff:
        parts = [p.strip() for p in xff.split(",")]
        return parts[-n] if len(parts) >= n else parts[0]
    return request.META.get("REMOTE_ADDR", "?")


def is_limited(request, scope, limit, window):
    """شمارنده‌ی ساده در cache: بیش از `limit` درخواست در `window` ثانیه → True."""
    key = f"rl:{scope}:{client_ip(request)}"
    if cache.add(key, 1, window):
        return False
    try:
        return cache.incr(key) > limit
    except ValueError:
        cache.set(key, 1, window)
        return False
