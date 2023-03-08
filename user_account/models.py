from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom Users Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, phone and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
           name=name,
           phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        """
        Creates and saves a superuser with the given email, name, phone and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom user module
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

