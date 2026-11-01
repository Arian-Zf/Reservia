from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Appointment, Service
from .slots import is_valid_slot


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "description", "price_from"]


class AppointmentSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "service", "service_name", "start_time", "status"]
        read_only_fields = ["id", "status"]

    def validate_service(self, service):
        if not service.is_active:
            raise serializers.ValidationError("این خدمت فعال نیست.")
        return service

    def validate_start_time(self, value):
        if not is_valid_slot(value):
            raise serializers.ValidationError("این زمان قابل رزرو نیست.")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        active = Appointment.objects.filter(
            user=user, status=Appointment.Status.BOOKED, start_time__gt=timezone.now()
        ).count()
        if active >= settings.BOOKING["MAX_ACTIVE_PER_USER"]:
            raise serializers.ValidationError("به سقف تعداد نوبت‌های فعال رسیده‌اید.")
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"start_time": "این زمان همین الان رزرو شد؛ زمان دیگری انتخاب کنید."})
