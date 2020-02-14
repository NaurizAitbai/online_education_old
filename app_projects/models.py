from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .projects import PROJECT_TYPES


PROJECT_TYPE_CHOICES = []
for types in PROJECT_TYPES.values():
    for code, name in types.items():
        PROJECT_TYPE_CHOICES.append([code, name])


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', verbose_name=_('Пользователь'))
    name = models.CharField(max_length=128, verbose_name=_('Имя проекта'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание проекта'))
    type = models.CharField(max_length=128, choices=PROJECT_TYPE_CHOICES, verbose_name=_('Тип проекта'))
    project_identifier = models.CharField(max_length=255, null=True, verbose_name=_('Идентификатор проекта'))
    project_folder = models.CharField(max_length=255, null=True, verbose_name=_('Расположение проекта'))


    class Meta:
        db_table = 'projects'
        verbose_name = _('проект')
        verbose_name_plural = _('проекты')