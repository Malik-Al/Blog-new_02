from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4


class Token(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='user',
                             related_name='registration_tokens')
    token = models.UUIDField(verbose_name='Token', default=uuid4)

    def __str__(self):
        return str(self.token)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'