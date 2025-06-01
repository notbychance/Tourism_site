import itertools

from rest_framework.routers import DefaultRouter
from transliterate import slugify as transliterate_slugify


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
    slug = transliterate_slugify(
        getattr(instance, source_field), language_code='ru')
    unique_slug = slug

    for i in itertools.count(1):
        if not instance.__class__.objects.filter(**{slug_field: unique_slug}).exists():
            break
        unique_slug = f'{slug}-{i}'

    return unique_slug
