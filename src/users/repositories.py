from core.exceptions import GeneralUserAlreadyExist
from core.exceptions import GeneralUserNotFound
from core.repositories import BaseRepository
from users.models import User


class UserRepository(BaseRepository):
    def create_user(self, phone_number: str, **data) -> User:
        if self.model.objects.filter(phone_number=phone_number).exists():
            raise GeneralUserAlreadyExist()
        return self.model.objects.create(phone_number=phone_number, **data)

    def get_user_by_number(self, phone_number: str) -> User:
        try:
            return self.model.objects.select_related("auth_token").get(phone_number=phone_number)
        except User.DoesNotExist:
            raise GeneralUserNotFound()

    @classmethod
    def factory(cls):
        return cls(User)
