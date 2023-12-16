# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# class Text(BaseContent):
#     body = models.TextField()

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


class Article(models.Model):
    THEMES = {
        ("Медицина", "Медицина"),
        ("Психология", "Психология"),
        ("Психотерапия", "Психотерапия"),
        ("Семейные отношения", "Семейные отношения"),
    }
    title = models.CharField("Заголовок", max_length=200)
    category = models.CharField("Категория", choices=THEMES, max_length=50)
    content = models.TextField("Контент")
    author = models.CharField("Автор", max_length=500, blank=True, null=True)
    time_for_read = models.IntegerField("Время, необходимое для прочтения")
    date = models.DateField("Дата написания")
    date_of_publishing = models.DateField("Дата, когда статья была выложена", auto_created=True)
    literature = models.TextField("Список литературы", blank=True, null=True)

    # tags
    def get_absolute_url(self):
        return f'/article/{self.pk}/'

    class Meta:
        db_table = "Статья"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['title']

class RecordGratitudeJournal(models.Model):
    content = models.CharField("Контент", max_length=300)
    to_whom = models.CharField("Кому", max_length=100)
    date = models.DateField(auto_now_add=True)

    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Автор")

    class Meta:
        db_table = "Записи Дневника Благодарности"
        verbose_name = "Запись Дневника Благодарности"
        verbose_name_plural = "Записи Дневника Благодарности"
        ordering = ['date']

class Slumber(models.Model):
    date = models.DateField("Дата")
    quality = models.IntegerField("Качество сна")
    duration = models.IntegerField("Продолжительность")
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Автор")

    class Meta:
        db_table = "Сон"
        verbose_name = "Сон"
        verbose_name_plural = "Сон"
        ordering = ['date']


