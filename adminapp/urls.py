from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReservationViewSet, 
    ClientRegistrationView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    # Include the router URLs
    path('api/', include(router.urls)),
    path('api/register/', ClientRegistrationView.as_view(), name='client_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]