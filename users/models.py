from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, Permission, Group
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, verbose_name='Email adress', blank=True, null=True)
    username = models.CharField(max_length=49, blank=True, null=True, verbose_name='User Name')
    first_name = models.CharField(u"First Name", max_length=100, blank=True, null=True)
    last_name = models.CharField(u"Last Name", max_length=100, blank=True, null=True)
    patronymic = models.CharField(u"Patronymic", max_length=100, blank=True, null=True)
    user_profile_id = models.IntegerField(blank=True, verbose_name='ID User', null=True)
    phone = models.CharField(max_length=24, blank=True, null=True, verbose_name='Phone')
    photo = models.ImageField(upload_to='midia/users/%Y/%m/%d/', blank=True, null=True, default='../static/assets/img/default_avatar.png',
                              verbose_name='Avatar')
    is_active = models.BooleanField(default=True, verbose_name='Activate', blank=True, null=True)
    is_admin = models.BooleanField(default=False, verbose_name='Administrator', blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False, blank=True, null=True)
    is_superuser = models.BooleanField(_('super user'), default=False, blank=True, null=True)
    date_joined = models.DateTimeField(u'date joined', blank=True, null=True, default=timezone.now)
    last_login = models.DateTimeField(u'last login', blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, verbose_name='Email adress', blank=True, null=True)
    verificated = models.BooleanField(default=False, blank=True, null=True)
    ADMINISTRATOR = 'AD'
    MANAGER = 'OA'
    CLIENT = 'CL'
    CLMANAGER = 'OO'

    TYPE_ROLE = [
        (ADMINISTRATOR, 'Administrator'),
        (MANAGER, 'Manager'),
        (CLIENT, 'Client'),
        (CLMANAGER, 'Client Manager')
    ]

    type = models.CharField(max_length=6, choices=TYPE_ROLE, default=CLIENT, verbose_name='Type User')
    ban = models.BooleanField(default=False, verbose_name='Baned')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name',]

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name}  {self.patronymic}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # db_table = 'users_customuser'

    def get_absolute_url(self):
        return reverse('user_info', kwargs={'user_id': self.id})

    # def save(self, *args, **kwargs):
    #     using = 'users'
    #     super(CustomUser, self).save(using=using, *args, **kwargs)


# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ С ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИЕЙ #
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    background = models.ImageField(upload_to="profiles/backgrounds/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'Users profiles'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def first_name(self):
        return self.user.first_name


class PlayProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Play User profile'
        verbose_name_plural = 'Play Users profiles'

    def get_absolute_url(self):
        return reverse('play_profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def first_name(self):
        return self.user.first_name

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        PlayProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.playprofile.save()
    
    
class AccessToken(models.Model):
    token = models.CharField(
        max_length=255,
    )
    user = models.ForeignKey(
        to='CustomUser',
        on_delete=models.CASCADE
    )