from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from .models import Appointment


def day_slots(day: date) -> list[datetime]:
    """Return all valid, timezone-aware appointment starts for a local date."""
    if not isinstance(day, date) or isinstance(day, datetime):
        return []

    today = timezone.localdate()
    days_ahead = settings.BOOKING["DAYS_AHEAD"]
    if day < today or day > today + timedelta(days=days_ahead - 1):
        return []
    if day.weekday() in settings.BOOKING["CLOSED_WEEKDAYS"]:
        return []

    tz = timezone.get_current_timezone()
    start_hour = settings.BOOKING["OPEN_HOUR"]
    close_hour = settings.BOOKING["CLOSE_HOUR"]
    step = settings.BOOKING["SLOT_MINUTES"]

    result = []
    current = datetime.combine(day, time(start_hour, 0), tzinfo=tz)
    end = datetime.combine(day, time(close_hour, 0), tzinfo=tz)
    now = timezone.now()

    while current < end:
        if current > now:
            result.append(current)
        current += timedelta(minutes=step)
    return result


def free_slots(day: date) -> list[datetime]:
    """Return valid starts not already occupied by an active appointment."""
    slots = day_slots(day)
    if not slots:
        return []
    occupied = set(
        Appointment.objects.filter(
            start_time__date=day,
        ).exclude(status=Appointment.Status.CANCELLED).values_list("start_time", flat=True)
    )
    return [slot for slot in slots if slot not in occupied]


def is_valid_slot(value: datetime) -> bool:
    """Check that a submitted datetime exactly matches an available slot."""
    if not isinstance(value, datetime) or timezone.is_naive(value):
        return False
    local_value = timezone.localtime(value)
    if local_value.second or local_value.microsecond:
        return False
    return any(slot == value for slot in free_slots(local_value.date()))
