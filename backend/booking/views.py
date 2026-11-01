from datetime import date

from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .models import Appointment, Service
from .serializers import AppointmentSerializer, ServiceSerializer
from .slots import free_slots


class ServiceListView(ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class SlotsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            day = date.fromisoformat(request.query_params.get("date", ""))
        except ValueError:
            return Response({"detail": "تاریخ نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
        return Response([s.isoformat() for s in free_slots(day)])


class AppointmentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AppointmentSerializer
    throttle_classes = [UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "booking"
    pagination_class = None

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user).select_related("service").order_by("-start_time")

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        appt = self.get_object()
        if appt.status != Appointment.Status.BOOKED or appt.start_time <= timezone.now():
            return Response({"detail": "این نوبت قابل لغو نیست."}, status=status.HTTP_400_BAD_REQUEST)
        appt.status = Appointment.Status.CANCELLED
        appt.save(update_fields=["status"])
        return Response(self.get_serializer(appt).data)
