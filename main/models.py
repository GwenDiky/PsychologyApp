# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Emotion(models.Model):
    moods = (("Злой", "Злой"),
             ("Грустный", "Грустный"),
             ("Нейтральный", "Нейтральный"),
             ("Игривый", "Игривый"),
             ("Недовольный", "Недовольный"),
             ("Довольный", "Довольный"),
             ("Очень довольный", "Очень довольный"),
             ("Агрессивный", "Агрессивный"),
             ("Кокетливый", "Кокетливый"),
             ("Грустный", "Грустный"),
             ("Очень грустный", "Очень грустный"),
             ("Ошарашенный", "Ошарашенный"),
             ("В смятении", "В сметянии"),
             ("В шоке", "В шоке"),
             ("Радостный", "Радостный"),)

    title = models.CharField("Наименование:",
                             max_length = 20,
                             choices=moods)
    effort = models.PositiveIntegerField("На сколько сильной была эмоция",
                                         validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateField("Дата")
    reason = models.TextField("После чего вы ее испытали",
                              blank=True,
                              null=True)

    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Настроение"
        verbose_name_plural = "Настроение"

        unique_together = ('author', 'date')


class Article(models.Model):
    THEMES = {
        ("Медицина", "Медицина"),
        ("Психология", "Психология"),
        ("Психотерапия", "Психотерапия"),
        ("Семейные отношения", "Семейные отношения"),
    }
    title = models.CharField("Заголовок",
                             max_length=200)
    category = models.CharField("Категория",
                                choices=THEMES,
                                max_length=50)
    content = models.TextField("Контент")
    author = models.CharField("Автор",
                              max_length=500,
                              blank=True,
                              null=True)
    time_for_read = models.IntegerField("Время, необходимое для прочтения")
    date = models.DateField("Дата написания")
    date_of_publishing = models.DateField("Дата, когда статья была выложена",
                                          auto_created=True)
    literature = models.TextField("Список литературы",
                                  blank=True,
                                  null=True)

    # tags
    def get_absolute_url(self):
        return f'/article/{self.pk}/'

    class Meta:
        db_table = "Статья"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['title']

class RecordGratitudeJournal(models.Model):
    content = models.CharField("Контент",
                               max_length=300)
    to_whom = models.CharField("Кому",
                               max_length=100)
    date = models.DateField(auto_now_add=True)

    author = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name="Автор")

    class Meta:
        db_table = "Записи Дневника Благодарности"
        verbose_name = "Запись Дневника Благодарности"
        verbose_name_plural = "Записи Дневника Благодарности"
        ordering = ['-date']

class Slumber(models.Model):
    date = models.DateField("Дата")
    quality = models.IntegerField("Качество сна",
                                  validators=[MinValueValidator(1), MaxValueValidator(5)])
    duration = models.IntegerField("Продолжительность",
                                   validators=[MinValueValidator(1), MaxValueValidator(24)])
    content = models.TextField("Примечания",
                               blank=True,
                               null=True)
    author = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name="Автор")

    class Meta:
        db_table = "Сон"
        verbose_name = "Сон"
        verbose_name_plural = "Сон"
        ordering = ['date']


class PhysicalActivity(models.Model):
    ACTIVITY = {
        ("Спортивная ходьба", "Спортивная ходьба"),
        ("Бокс", "Бокс"),
        ("Кардио-тренировка", "Кардио-тренировака"),
        ("Силовая тренировка", "Силовая тренировка"),
        ("Теннис", "Теннис"),
        ("Бег", "Бег"),
        ("Футбол", "Футбол"),
        ("Баскетбол", "Баскетбол"),
        ("Йога", "Йога"),
    }
    INTENSITY = {
        ("Низкая", "Низкая"),
        ("Средняя", "Средняя"),
        ("Высокая", "Высокая"),
    }
    average_pulse = models.PositiveIntegerField("Средний пульс",
                                        blank=True,
                                        null=True)
    type_of_activity = models.CharField("Тип активности",
                                        max_length=100,
                                        choices=ACTIVITY)
    duration = models.PositiveIntegerField("Продолжительность")
    intensity = models.CharField("Интенсивность",
                                 choices=INTENSITY,
                                 max_length=100)
    state_after = models.CharField("Состояние после тренировки:",
                                    max_length=250,
                                    null=True,
                                    blank=True)
    date = models.DateField("Дата")

    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               verbose_name='Автор',
                               )

    class Meta:
        db_table = "Активность"
        verbose_name = "Физическая нагрузка"
        verbose_name_plural = "Физические нагрузки"
        ordering = ['-date']

