from rest_framework import serializers

from users.models import User
from users.utils import phone_number_validators


class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(source="auth_token.key", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "father_name",
            "birth_date",
            "gender",
            "access_token",
        )
        read_only_fields = (
            "phone_number",
            "access_token",
        )
        extra_kwargs = {
            "first_name": {"required": True, "allow_null": False},
        }


class PhoneNumberVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_number_validators])


class FirebaseTokenSerializer(serializers.Serializer):
    firebase_token = serializers.CharField(required=True)


class UserRegistrationSerializer(FirebaseTokenSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "father_name",
            "birth_date",
            "gender",
            "firebase_token",
        )
        extra_kwargs = {
            "first_name": {"required": True, "allow_null": False},
        }


class UserLoginSerializer(FirebaseTokenSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("firebase_token",)
