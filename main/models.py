# Create your models here.
from django.db import models


class Mood(models.Model):
    moods = (("angry", "Злой"),
             ("sad", "Грустный"),
             ("neutral", "Нейтральный"))

    title = models.CharField("Наименование:", max_length = 20, choices=moods)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Настроение"
        verbose_name_plural = "Настроение"