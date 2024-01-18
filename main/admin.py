from django.contrib import admin
from .models import (
    Article, RecordGratitudeJournal, Slumber,
    PhysicalActivity, Emotion)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    search_fields = ['title']
    list_filter = ['date_of_publishing', 'date', 'category', 'time_for_read']
    list_display_links = ('title',)


@admin.register(RecordGratitudeJournal)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'to_whom', 'author']
    search_fields = ['date', 'author', 'content']
    list_filter = ['date', 'author']

@admin.register(Slumber)
class SlumberAdmin(admin.ModelAdmin):
    list_display = ['date', 'duration', 'author']
    search_fields = ['author', 'date', 'duration']
    list_filter = ['author', 'date', 'duration']

@admin.register(PhysicalActivity)
class PhysicalActivityAdmin(admin.ModelAdmin):
    list_display = ['date', 'type_of_activity']
    search_fields = ['date', 'state_after']
    list_filter = (['date', 'type_of_activity', 'intensity', 'average_pulse', 'duration'])

@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'reason']
    search_fields = ['date', 'state_after']
    list_filter = ['date', 'reason', 'author', 'effort', 'title',]