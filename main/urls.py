from django.urls import path

from .views import (home, ArticleList, ArticleDetail, MoodList)
app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('articles', ArticleList.as_view(template_name="article/articles_list.html"), name='articles'),
    path('article/<int:id>', ArticleDetail.as_view(template_name="article/article.html"), name='article'),
    path('moods', MoodList.as_view(template_name="trackers/mood.html"), name='moods'),
    path('sleeping', MoodList.as_view(template_name="trackers/sleeping.html"), name='sleeping'),
]