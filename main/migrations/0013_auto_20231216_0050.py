# Generated by Django 3.2.23 on 2023-12-15 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_auto_20231216_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Психология', 'Психология'), ('Медицина', 'Медицина'), ('Психотерапия', 'Психотерапия'), ('Семейные отношения', 'Семейные отношения')], max_length=50, verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='Slumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('quality', models.IntegerField(verbose_name='Качество сна')),
                ('duration', models.IntegerField(verbose_name='Продолжительность')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Сон',
                'verbose_name_plural': 'Сон',
                'db_table': 'Сон',
                'ordering': ['date'],
            },
        ),
    ]
