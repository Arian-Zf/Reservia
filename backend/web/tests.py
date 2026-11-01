from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from booking.models import Appointment, Service


class PagesTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name="کراتینه", price_from=2500000, icon="hair")
        self.user = get_user_model().objects.create_user("sara", password="S3cure-pass-998", first_name="سارا")

    def test_public_pages(self):
        for name in ("/", "/services/", "/login/", "/register/"):
            self.assertEqual(self.client.get(name).status_code, 200, name)

    def test_home_shows_service_with_persian_price(self):
        self.assertContains(self.client.get("/"), "۲٬۵۰۰٬۰۰۰")

    def test_book_requires_login(self):
        r = self.client.get("/book/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r["Location"])

    def test_register_logs_in(self):
        r = self.client.post("/register/", {"first_name": "مینا", "username": "mina", "password1": "Tr1cky-pass-77", "password2": "Tr1cky-pass-77"})
        self.assertRedirects(r, "/book/", fetch_redirect_response=False)
        self.assertEqual(self.client.get("/book/").status_code, 200)

    def test_my_page_and_cancel_only_own(self):
        other = get_user_model().objects.create_user("other", password="S3cure-pass-998")
        appt = Appointment.objects.create(user=other, service=self.service, start_time=timezone.now() + timedelta(days=2))
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/my/").status_code, 200)
        self.assertEqual(self.client.post(f"/my/{appt.id}/cancel/").status_code, 404)
        mine = Appointment.objects.create(user=self.user, service=self.service, start_time=timezone.now() + timedelta(days=3))
        self.assertContains(self.client.get("/my/"), "کراتینه")
        self.client.post(f"/my/{mine.id}/cancel/")
        mine.refresh_from_db()
        self.assertEqual(mine.status, "cancelled")
