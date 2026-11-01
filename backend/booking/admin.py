from django.contrib import admin

from .models import Appointment, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "price_from", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "icon")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("start_time", "user", "service", "status")
    list_filter = ("status", "service")
    search_fields = ("user__username", "user__first_name")
    date_hierarchy = "start_time"
