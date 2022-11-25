from django.db import models

# Create your models here.

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    to = reset_password_token.user.email
    subject, from_email= 'Password reset Token', 'indrakhanal291@gmail.com'
    text_content = f'Please Use the following code to reset your password.<br><h1>{reset_password_token.key}</h1>'
    # html_content = '<p>Do not share this code to <strong>Anyone</strong></p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(text_content, "text/html")
    # msg.attach_alternative(html_content, "text/html")
    msg.send()

    # send an e-mail to the user
    # context = {
    #     'current_user': reset_password_token.user,
    #     'username': reset_password_token.user.username,
    #     'email': reset_password_token.user.email,
    #     'reset_password_url': "{}?token={}".format(
    #         instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #         reset_password_token.key)
    # }
    

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        super_user_check = extra_fields.get('is_superuser')
        if super_user_check is True:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        else:
            phone = extra_fields.get('phone', None)
            if not phone:
                raise ValueError(_('phone number must be set'))
            if not email:
                raise ValueError(_('The Email must be set'))
            email = self.normalize_email(email)
            user = self.model(email=email,  phone=phone, **extra_fields)
            user.set_password(password)
            user.save()
            return user


    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # extra_fields.setdefault('phone', None)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('contact'), max_length=15, unique=True, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

