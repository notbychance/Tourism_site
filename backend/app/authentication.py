from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions


class CustomerJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """Возвращает Customer на основе данных из токена."""
        try:
            from app.models import Customer
            login = validated_token.get('login')
            return Customer.objects.get(login=login)
        except Customer.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь не найден')