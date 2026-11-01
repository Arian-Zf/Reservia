from django.conf import settings
from django.db import models
from django.db.models import Q


class Service(models.Model):
    class Icon(models.TextChoices):
        HAIR = "hair", "مو"
        SKIN = "skin", "پوست"
        NAILS = "nails", "ناخن"
        MAKEUP = "makeup", "آرایش"
        BRIDE = "bride", "عروس"
        SPA = "spa", "اسپا و ریلکسیشن"

    name = models.CharField("نام خدمت", max_length=100)
    description = models.TextField("توضیح کوتاه", blank=True)
    price_from = models.PositiveIntegerField("قیمت از (تومان)", null=True, blank=True)
    icon = models.CharField("آیکن", max_length=10, choices=Icon.choices, default=Icon.HAIR)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Appointment(models.Model):
    class Status(models.TextChoices):
        BOOKED = "booked", "رزرو شده"
        CANCELLED = "cancelled", "لغو شده"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    start_time = models.DateTimeField("زمان شروع", db_index=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"
        ordering = ["start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["start_time"],
                condition=~Q(status="cancelled"),
                name="unique_active_slot",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.start_time:%Y-%m-%d %H:%M}"
