# core/utils/slug_helpers.py
import itertools

from rest_framework.routers import DefaultRouter
from transliterate import slugify as transliterate_slugify
from django.contrib.auth.models import BaseUserManager


class SlugRouter(DefaultRouter):
    def get_lookup_regex(self, viewset, lookup_prefix=''):
        base_regex = super().get_lookup_regex(viewset, lookup_prefix)
        if viewset.lookup_field == 'slug':
            return r'(?P<{lookup_prefix}slug>[-\w]+)'.format(
                lookup_prefix=lookup_prefix
            )
        return base_regex


def unique_slugify(instance, slug_field, source_field):
    """
    Генерация уникального slug на основе source_field.
    Автоматически добавляет суффикс (-1, -2) при дубликатах.
    """
    slug = transliterate_slugify(getattr(instance, source_field), language_code='ru')
    unique_slug = slug

    for i in itertools.count(1):
        if not instance.__class__.objects.filter(**{slug_field: unique_slug}).exists():
            break
        unique_slug = f'{slug}-{i}'

    return unique_slug


class CustomerManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        customer = self.model(
            email=self.normalize_email(email),
            login=login,
            **extra_fields
        )
        customer.set_password(password)
        customer.save(using=self._db)
        return customer