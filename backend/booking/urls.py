from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("appointments", views.AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("services/", views.ServiceListView.as_view()),
    path("slots/", views.SlotsView.as_view()),
    path("", include(router.urls)),
]
