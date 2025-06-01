import itertools

from rest_framework.routers import DefaultRouter
from transliterate import slugify as transliterate_slugify


class CustomRouter(DefaultRouter):
    def get_lookup_regex(self, viewset, lookup_prefix=''):
        base_regex = super().get_lookup_regex(viewset, lookup_prefix)
        if getattr(viewset, 'lookup_field', None) == 'slug':
            return r'(?P<{lookup_prefix}slug>[-\w]+)'.format(
                lookup_prefix=lookup_prefix
            )
        return base_regex
    
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        
        if getattr(viewset, 'lookup_field', None) == 'slug':
            for route in routes:
                if '{lookup_field}' in route.url:
                    route.url = route.url.replace(
                        '{lookup_field}',
                        '{slug}'
                    )
        
        return routes
    
    def get_urls(self):
        urls = super().get_urls()        
        return urls


def unique_slugify(instance, slug_field, source_field):
    slug = transliterate_slugify(
        getattr(instance, source_field), language_code='ru')
    unique_slug = slug

    for i in itertools.count(1):
        if not instance.__class__.objects.filter(**{slug_field: unique_slug}).exists():
            break
        unique_slug = f'{slug}-{i}'

    return unique_slug
