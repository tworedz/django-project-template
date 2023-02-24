from dataclasses import dataclass

from django.db import transaction
from rest_framework.authtoken.models import Token

from core.exceptions import GeneralUserNotFound
from firebase_auth.mixins import FirebaseAuthMixin
from users.models import User


@dataclass
class UserVerificationService:
    def create_user_by_firebase_token(self, **user_data) -> User:
        """
        :raise ValueError: Если пользователь firebase отключен.
        """
        firebase_token = user_data.pop("firebase_token")
        phone_number = self.validate_firebase_token(firebase_token)
        with transaction.atomic():
            user = self.user_repository.create_user(phone_number=phone_number, **user_data)
            Token.objects.get_or_create(user=user)
            self.barcode_service.factory().generate_barcode(user=user)
            return self.user_repository.get_user_by_number(phone_number)

    def get_user_by_firebase_token(self, firebase_token: str) -> User:
        phone_number = self.validate_firebase_token(firebase_token)
        return self.user_repository.get_user_by_number(phone_number)

    def validate_firebase_token(self, firebase_token: str) -> str:
        uid = FirebaseAuthMixin.validate_id_token(firebase_token)
        return self.firebase_auth.get_phone(uid)

    def get_registration_status(self, phone_number: str) -> bool:
        try:
            self.user_repository.get_user_by_number(phone_number=phone_number)
        except GeneralUserNotFound:
            return False
        else:
            return True
