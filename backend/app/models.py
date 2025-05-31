import datetime

from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.db.models.manager import Manager
from django.contrib.auth.models import AbstractBaseUser

from app.addons import unique_slugify, CustomerManager


# Create your models here.
class Customer(AbstractBaseUser):
    credentials = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=50, unique=True,
                             validators=[RegexValidator(
                                 regex='^[a-zA-Z0-9_]+$',
                                 message='Логин может содержать только буквы, цифры и подчеркивания'
                             )])  # ваши валидаторы
    phone = models.CharField(max_length=15)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'credentials']

    objects = CustomerManager()

    def __str__(self):
        return self.credentials


class SocialMediaType(models.Model):
    type = models.CharField(max_length=120, unique=True)

    objects: Manager = models.Manager()

    def __str__(self):
        return self.type


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=11,
                             validators=[
                                 RegexValidator(
                                     regex=r'^\+?1?\d{9,15}$',
                                     message="Номер телефона должен быть в формате: '+999999999'. Допускается до 15 цифр.")
                             ])
    address = models.TextField()
    slug = models.SlugField(unique=True, blank=False, editable=False)

    objects: Manager = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, 'slug', 'name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SocialMedia(models.Model):
    media_type = models.ForeignKey(SocialMediaType, on_delete=models.CASCADE)
    reference = models.CharField(max_length=120, unique=True, default="")
    target = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_to = models.DateTimeField(editable=False)

    objects: Manager = models.Manager()

    def save(self, *args, **kwargs):
        self.date_to = datetime.datetime.now() + datetime.timedelta(days=365)
        super().save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=120, unique=True)

    objects: Manager = models.Manager()

    def __str__(self):
        return self.name


class Tour(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=False, editable=False)
    img_preview_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=120)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    objects: Manager = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, 'slug', 'title')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TourInfo(models.Model):
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    img_url = models.URLField()
    img_background_url = models.URLField()
    placed = models.TextField()

    objects: Manager = models.Manager()


class TourTimeSpan(models.Model):
    group_name = models.CharField(max_length=100)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    place_count = models.IntegerField()

    objects: Manager = models.Manager()


class ReservationStatus(models.Model):
    # Константы значений (хранятся в БД)
    PAID = 'paid'
    DECLINED = 'declined'
    COMPLETED = 'completed'
    WAITING = 'waiting'
    MOVED = 'moved'
    PAID_BACK = 'paid_back'
    DIDNT_COME = 'no_show'

    # Кортежи для choices (значение БД, отображаемое имя)
    STATUS_CHOICES = [
        (PAID, 'Оплачено'),
        (COMPLETED, 'Завершено'),
        (DIDNT_COME, 'Клиент не явился'),
        (WAITING, 'Ожидание оплаты'),
        (PAID_BACK, 'Возврат средств'),
        (MOVED, 'Перенесено'),
        (DECLINED, 'Отклонено')
    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, unique=True)

    objects: Manager = models.Manager()

    def __str__(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    target = models.ForeignKey(TourTimeSpan, on_delete=models.CASCADE)
    status = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE)

    objects: Manager = models.Manager()


class Favourites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    target = models.ForeignKey(Tour, on_delete=models.CASCADE)

    objects: Manager = models.Manager()


class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    target = models.ForeignKey(Tour, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    objects: Manager = models.Manager()
