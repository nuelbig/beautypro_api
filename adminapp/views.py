from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import rdv
from .serializers import ReservationSerializer, ClientRegistrationSerializer

class ClientRegistrationView(generics.CreateAPIView):
    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return rdv.objects.all().order_by('-date', '-heure')
        return rdv.objects.filter(client_account=user).order_by('-date', '-heure')
    
    def perform_create(self, serializer):
        # Link reservation to the currently logged in user if they are a client
        if not self.request.user.is_staff:
             serializer.save(client_account=self.request.user, client=f"{self.request.user.first_name} {self.request.user.last_name}".strip() or self.request.user.username)
        else:
             serializer.save()

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'CONFIRMED'
        reservation.save()
        return Response({'status': 'reservation confirmed'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'REJECTED'
        reservation.save()
        return Response({'status': 'reservation rejected'})