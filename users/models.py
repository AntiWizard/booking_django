from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models, transaction

from reservations.base_models.address import AbstractAddress


class CustomUserManager(UserManager):
    def _create_user(self, phone, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError("The given phone must be set")
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, email, password, **extra_fields)


def validation_address_phone(value):
    if value:
        if not User.objects.filter(phone=value).exists():
            raise ValidationError(
                'User with %(value)s not exist',
                params={'value', value},
            )
        if not UserAddress.objects.filter(phone=value).exists():
            raise ValidationError(
                'Address for %(value)s not exist',
                params={'value', value},
            )


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "MALE"
        FEMALE = "FEMALE"

    username = None
    email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{8,14}$',
                                 message="Phone number must not consist of space and requires country code. eg : "
                                         "989210000000")
    phone = models.CharField(validators=[phone_regex], max_length=16, unique=True)
    birth_day = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True)
    nationality = models.CharField(max_length=40, null=True, blank=True)
    national_id = models.CharField(max_length=10, null=True, blank=True)
    avatar = models.ImageField(upload_to='auth/avatars/', null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    @transaction.atomic
    def save(self, *args, **kwargs):
        user_address = UserAddress.objects.filter(phone=self.phone)
        if not user_address.exists():
            user_address.create(phone=self.phone)
        super().save(*args, **kwargs)


class UserAddress(AbstractAddress):
    location = None

    def __str__(self):
        return self.phone
