from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import PhoneNumberVerificationSerializer
from users.serializers import UserLoginSerializer
from users.serializers import UserRegistrationSerializer
from users.serializers import UserSerializer
from users.services import UserVerificationService


class PhoneNumberVerificationAPIView(generics.GenericAPIView):
    serializer_class = PhoneNumberVerificationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: inline_serializer(
                name="PasscodeResponse",
                fields={
                    "is_registered": serializers.BooleanField(),
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_status = UserVerificationService.factory().get_registration_status(
            **serializer.validated_data,
        )
        return Response({"is_registered": auth_status}, status=status.HTTP_200_OK)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = (
        "get",
        "patch",
        "delete",
    )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = False
        return super().update(request, *args, **kwargs)


class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={201: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserVerificationService.factory().create_user_by_firebase_token(
            **serializer.validated_data,
        )

        return Response(
            UserSerializer(user, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserVerificationService.factory().get_user_by_firebase_token(
            **serializer.validated_data,
        )

        return Response(
            UserSerializer(user, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )
