from rest_framework import serializers
from .models import rdv, PasswordResetToken
from django.contrib.auth.models import User

class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'phone']

    def create(self, validated_data):
        # Use phone as username for clients to ensure uniqueness and simple login
        user = User.objects.create_user(
            username=validated_data['phone'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = rdv
        fields = '__all__'


class PasswordResetRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Phone number or email")

    def validate_identifier(self, value):
        # Try to find user by username (phone) or email
        user = User.objects.filter(username=value).first() or User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("Aucun utilisateur trouvé avec cet identifiant.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(token=value)
            if not reset_token.is_valid():
                raise serializers.ValidationError("Ce lien de réinitialisation a expiré ou a déjà été utilisé.")
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Lien de réinitialisation invalide.")
        return value
