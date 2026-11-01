import django.conf
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="نام خدمت")),
                ("is_active", models.BooleanField(default=True, verbose_name="فعال")),
            ],
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_time", models.DateTimeField(db_index=True, verbose_name="زمان شروع")),
                ("status", models.CharField(choices=[("booked", "رزرو شده"), ("cancelled", "لغو شده")], default="booked", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="booking.service")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="appointments", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "نوبت",
                "verbose_name_plural": "نوبت‌ها",
                "ordering": ["start_time"],
                "constraints": [
                    models.UniqueConstraint(
                        condition=~models.Q(("status", "cancelled")),
                        fields=("start_time",),
                        name="unique_active_slot",
                    ),
                ],
            },
        ),
    ]
