from rest_framework import serializers
from .models import rdv
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
