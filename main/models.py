# Create your models here.
from django.db import models



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
        ("Психология", "Психология")
    }
    title = models.CharField("Заголовок", max_length=200)
    c1ategory = models.CharField("Категория", choices=THEMES, max_length=50)
    content = models.TextField("Контент")
    time_for_read = models.IntegerField("Время, необходимое для прочтения")
    date = models.DateField("Дата написания")
    date_of_publishing = models.DateField("Дата, когда статья была выложена", auto_created=True)

    # tags
    def get_abosule_url(self):
        return "/main/%s" % self.pk

    class Meta:
        db_table = "Статья"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['title']
