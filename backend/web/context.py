from django.conf import settings


def salon(request):
    return {"SALON": settings.SALON}
