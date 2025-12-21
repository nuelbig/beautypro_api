from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import rdv, PasswordResetToken
from .serializers import (
    ReservationSerializer, 
    ClientRegistrationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from django.contrib.auth.models import User
import secrets

class ClientRegistrationView(generics.CreateAPIView):
    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return rdv.objects.all().order_by('created_at')
        return rdv.objects.filter(client_account=user).order_by('created_at')
    
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
        # Get rejection reason from request body
        rejection_reason = request.data.get('rejection_reason', '')
        if rejection_reason:
            reservation.rejection_reason = rejection_reason
        reservation.save()
        return Response({'status': 'reservation rejected', 'rejection_reason': rejection_reason})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone', '')
        
        if not phone:
            return Response({
                'error': 'Numéro de téléphone requis.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find user by username (phone)
        user = User.objects.filter(username=phone).first()
        
        if user:
            return Response({
                'message': 'Numéro vérifié.',
                'phone': phone
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Aucun compte trouvé avec ce numéro.'
            }, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone', '')
        new_password = request.data.get('new_password', '')
        confirm_password = request.data.get('confirm_password', '')
        
        if not phone or not new_password or not confirm_password:
            return Response({
                'error': 'Tous les champs sont requis.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({
                'error': 'Les mots de passe ne correspondent pas.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 6:
            return Response({
                'error': 'Le mot de passe doit contenir au moins 6 caractères.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find user by username (phone)
        user = User.objects.filter(username=phone).first()
        
        if user:
            # Reset password
            user.set_password(new_password)
            user.save()
            
            return Response({
                'message': 'Mot de passe réinitialisé avec succès.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Aucun compte trouvé avec ce numéro.'
            }, status=status.HTTP_404_NOT_FOUND)
