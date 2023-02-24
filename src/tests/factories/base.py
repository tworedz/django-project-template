from django.utils import timezone
import factory


class BaseFactory(factory.django.DjangoModelFactory):
    created_at = factory.LazyFunction(lambda: timezone.now())
    updated_at = factory.LazyFunction(lambda: timezone.now())
