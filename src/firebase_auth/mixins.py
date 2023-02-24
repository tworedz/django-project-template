import logging

from django.utils.encoding import force_text
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError

from core.exceptions import GeneralFirebaseError
from core.exceptions import GeneralBadRequest
from core.exceptions import GeneralNotFound


logger = logging.getLogger(__name__)


class FirebaseAuthMixin:
    @staticmethod
    def validate_id_token(value: str):
        try:
            token = force_text(value)
            decoded_token = auth.verify_id_token(token)
            firebase_user = auth.get_user(decoded_token["uid"])
            if not firebase_user.disabled:
                return firebase_user.uid
            raise ValueError("we expect enabled user")
        except (
            ValueError,
            auth.InvalidIdTokenError,
            auth.ExpiredIdTokenError,
            auth.UserDisabledError,
            auth.UserNotFoundError,
        ):
            raise GeneralFirebaseError()
        except Exception:
            logger.exception("Unexpected exception while validating token")
            raise GeneralBadRequest()


class FirebaseAuthService:
    @classmethod
    def get_phone(cls, uid: str):
        try:
            return auth.get_user(uid).phone_number
        except UserNotFoundError:
            raise GeneralNotFound()
