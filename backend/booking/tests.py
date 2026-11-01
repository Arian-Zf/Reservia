from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Service
from .slots import day_slots


class BookingApiTests(APITestCase):
    def setUp(self):
        self.service = Service.objects.create(name="مشاوره")
        self.user = get_user_model().objects.create_user("ali", password="S3cure-pass-998")
        self.client.force_authenticate(self.user)

    def _free_slot(self):
        for i in range(1, 10):
            slots = day_slots(timezone.localdate() + timedelta(days=i))
            if slots:
                return slots[0]

    def test_book_then_double_book_fails_then_cancel(self):
        slot = self._free_slot()
        r = self.client.post("/api/appointments/", {"service": self.service.id, "start_time": slot.isoformat()})
        self.assertEqual(r.status_code, 201)
        r2 = self.client.post("/api/appointments/", {"service": self.service.id, "start_time": slot.isoformat()})
        self.assertEqual(r2.status_code, 400)
        self.assertEqual(self.client.post(f"/api/appointments/{r.data['id']}/cancel/").status_code, 200)
        r3 = self.client.post("/api/appointments/", {"service": self.service.id, "start_time": slot.isoformat()})
        self.assertEqual(r3.status_code, 201)

    def test_invalid_time_rejected(self):
        bad = (timezone.now() + timedelta(days=1)).replace(minute=7, second=0, microsecond=0)
        r = self.client.post("/api/appointments/", {"service": self.service.id, "start_time": bad.isoformat()})
        self.assertEqual(r.status_code, 400)

    def test_requires_auth(self):
        self.client.force_authenticate(None)
        self.assertIn(self.client.get("/api/appointments/").status_code, (401, 403))
