from typing import Generic
from typing import List
from typing import TypeVar
from typing import Union

from django.db import models
from django.db.models import QuerySet

from core.exceptions import GeneralNotFound


T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: models.Model

    def __init__(self, model: T):
        self.model = model

    def get_by_id(self, instance_id: int or str) -> T:
        return self.get_one(id=instance_id)

    def get_one(self, **kwargs) -> T:
        try:
            return self.model.objects.get(**kwargs)
        except models.ObjectDoesNotExist:
            raise GeneralNotFound()

    def filter(self, **kwargs) -> Union[QuerySet, List[T]]:  # noqa: A003
        return self.model.objects.filter(**kwargs)

    def create(self, **data) -> T:
        instance = self.model(**data)
        instance.save()
        return instance
