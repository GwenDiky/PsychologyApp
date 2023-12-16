# Generated by Django 3.2.23 on 2023-12-12 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_article_c1ategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='c1ategory',
            new_name='category',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Автор'),
        ),
    ]
