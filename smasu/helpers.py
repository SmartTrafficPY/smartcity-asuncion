from django.contrib.auth.models import User
from django.core.cache import caches
from django.urls import reverse


class CacheHelper:
    cache_key = "default"

    @classmethod
    def get_object(cls, obj_key, obj_cls, kwargs):
        obj = caches[cls.cache_key].get(obj_key)
        if obj is None:
            obj = obj_cls.objects.get(**kwargs)

        caches[cls.cache_key].set(obj_key, obj)
        return obj


def as_entity(obj):
    if isinstance(obj, User):
        return reverse("entities:users", args=(obj.pk,))

    as_entity = getattr(obj, "as_entity")
    return as_entity()
