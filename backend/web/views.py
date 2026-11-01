from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from booking.models import Appointment, Service

from .forms import RegisterForm, StyledAuthForm
from .ratelimit import is_limited


def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, "web/home.html", {"services": services})


def services(request):
    return render(request, "web/services.html", {"services": Service.objects.filter(is_active=True)})


@login_required
def book(request):
    return render(request, "web/book.html", {"initial_service": request.GET.get("service", "")})


@login_required
def my_appointments(request):
    now = timezone.now()
    qs = Appointment.objects.filter(user=request.user).select_related("service")
    upcoming = qs.filter(status=Appointment.Status.BOOKED, start_time__gt=now).order_by("start_time")
    past = qs.exclude(status=Appointment.Status.BOOKED, start_time__gt=now).order_by("-start_time")[:20]
    return render(request, "web/my_appointments.html", {"upcoming": upcoming, "past": past})


@login_required
@require_POST
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, user=request.user)  # فقط نوبت خود کاربر
    if appt.status == Appointment.Status.BOOKED and appt.start_time > timezone.now():
        appt.status = Appointment.Status.CANCELLED
        appt.save(update_fields=["status"])
        messages.success(request, "نوبت شما لغو شد.")
    else:
        messages.error(request, "این نوبت قابل لغو نیست.")
    return redirect("my_appointments")


class LoginView(DjangoLoginView):
    template_name = "web/login.html"
    authentication_form = StyledAuthForm
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        if is_limited(request, "login", 10, 300):
            form = self.get_form()
            form.add_error(None, "تلاش‌های ناموفق زیاد بود؛ چند دقیقه‌ی دیگر دوباره امتحان کنید.")
            return self.render_to_response(self.get_context_data(form=form), status=429)
        return super().post(request, *args, **kwargs)


def register(request):
    if request.user.is_authenticated:
        return redirect("book")
    form = RegisterForm(request.POST or None)
    status = 200
    if request.method == "POST":
        if is_limited(request, "register", 10, 3600):
            form.add_error(None, "تعداد ثبت‌نام از این شبکه زیاد بود؛ بعداً دوباره امتحان کنید.")
            status = 429
        elif form.is_valid():
            login(request, form.save())
            return redirect("book")
    return render(request, "web/register.html", {"form": form}, status=status)
