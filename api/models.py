from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self, email, password=None):
        """
          Creates and saves a super user
          with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_activated = True
        user.save()
        return user

    def create_staffuser(self, email, password=None):
        """
          Creates and saves a staff user
          with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_activated = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        blank=True,
        unique=True
    )
    phone_number = models.CharField(
        max_length=25,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        null=True
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        null=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="This is a staff level access"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="This blocks a user at the portal.\
                   The user has no influence on that."
    )
    is_activated = models.BooleanField(
        default=False,
        help_text="This is a user side activation via Phone or Email."
    )
    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, Auth):
        # "Does the user have permissions to view the app Auth?"
        # Simplest possible answer: Yes, always
        return True


class CustomerProfile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='customer', )
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.first_name + ' ' +  self.last_name


class CustomerTransaction(models.Model):
    owner = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE, related_name='transactions',)
    title = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=500,null=True)
    value = models.CharField(max_length=200,null=True)
    purchase_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(
        choices=[('p', 'Paid'), ('u', 'Unpaid'), ],
        max_length=2,
        default='u'
    )

    class Meta:
        ordering = ['purchase_date']

    def __str__(self):
        return self.title