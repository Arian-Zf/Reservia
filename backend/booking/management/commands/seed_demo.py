from django.core.management.base import BaseCommand

from booking.models import Service

DEMO = [
    ("رنگ و مش مو", "hair", 1800000, "رنگ‌های روز با محصولات اصل؛ مشاوره‌ی رنگ و مدل قبل از شروع کار."),
    ("کوتاهی و براشینگ", "hair", 450000, "مدل‌دهی متناسب با فرم صورت و سبک زندگی شما."),
    ("کراتینه و احیای مو", "hair", 2500000, "ترمیم عمیق و درخشندگی ماندگار برای موهای آسیب‌دیده."),
    ("مانیکور و پدیکور", "nails", 600000, "مراقبت کامل از دست و پا با ابزار کاملاً ضدعفونی‌شده."),
    ("کاشت و طراحی ناخن", "nails", 900000, "طرح‌های اختصاصی، از ساده و کلاسیک تا خاص و هنری."),
    ("پاکسازی و جوانسازی پوست", "skin", 1200000, "پوستی شفاف و شاداب با پروتکل‌های تخصصی."),
    ("میکاپ و شینیون عروس", "bride", 6000000, "روز خاص شما با هماهنگی کامل آرایش، مو و ماندگاری بالا."),
    ("اصلاح و لیفت ابرو", "makeup", 300000, "فرم‌دهی طبیعی که چهره را بازتر و جوان‌تر نشان می‌دهد."),
]


class Command(BaseCommand):
    help = "چند خدمت نمونه برای دیدن ظاهر سایت می‌سازد (قابل اجرای مجدد)."

    def handle(self, *args, **opts):
        for i, (name, icon, price, desc) in enumerate(DEMO):
            Service.objects.get_or_create(
                name=name, defaults={"icon": icon, "price_from": price, "description": desc, "order": i}
            )
        self.stdout.write(self.style.SUCCESS(f"{len(DEMO)} خدمت نمونه آماده است."))
