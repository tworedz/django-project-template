from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from users.views import PhoneNumberVerificationAPIView
from users.views import UserLoginAPIView
from users.views import UserRegistrationAPIView
from users.views import UserRetrieveUpdateDestroyAPIView


urlpatterns = [
    path("me/", UserRetrieveUpdateDestroyAPIView.as_view(), name="user-retrieve-update-delete"),
    path(
        "phone-number-verification/",
        PhoneNumberVerificationAPIView.as_view(),
        name="verification",
    ),
    path(
        "devices/",
        FCMDeviceAuthorizedViewSet.as_view({"post": "create"}),
        name="create_fcm_device",
    ),
    path(
        "firebase/register/",
        UserRegistrationAPIView.as_view(),
        name="firebase-registration",
    ),
    path(
        "firebase/login/",
        UserLoginAPIView.as_view(),
        name="firebase-login",
    ),
]
