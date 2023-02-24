import logging

from django.apps import AppConfig
from django.conf import settings
import firebase_admin


logger = logging.getLogger(__name__)


class FirebaseAuthConfig(AppConfig):
    name = "firebase_auth"

    def ready(self):
        try:
            cred = firebase_admin.credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
            firebase_admin.initialize_app(credential=cred)
        except FileNotFoundError:
            logger.warning("Firebase app not initialized!")
        else:
            logger.warning("Firebase app configured successfully!")
