from django.urls import path

from .views import (home, ArticleList, ArticleDetail, MoodList, PhysicalActivityList, SleepList,
                    Entry, TestsList, SearchResultsView, GratitudeJournalList, GratitudeJournalCreateView,
                    SlumberList)
app_name = 'main'

urlpatterns = [
    path('', home, name='home'),

    path('articles', ArticleList.as_view(template_name="article/articles_list.html"), name='articles'),
    path('articles/search', SearchResultsView.as_view(template_name="article/articles_list.html"), name='article_search'),
    path('article/<int:pk>/', ArticleDetail.as_view(template_name="article/article.html"), name='article'),

    path('moods', MoodList.as_view(template_name="trackers/mood.html"), name='moods'),

    path('sleeping', SlumberList.as_view(template_name="trackers/sleeping_new.html"), name='sleeping'),

    path('activity', PhysicalActivityList.as_view(template_name="trackers/physical_activity.html"), name='activity'),

    path('tests', TestsList.as_view(template_name="test/tests.html"), name='tests'),

    path('diary/text-editor', GratitudeJournalCreateView.as_view(template_name="diary/text_editor.html"), name='text-editor'),
    path('diary', GratitudeJournalList.as_view(template_name="diary/diary.html"), name='diary'),


    path('profile', TestsList.as_view(template_name="profile.html"), name='profile'),
    path('signin', TestsList.as_view(template_name="sign_in.html"), name='signin'),
    path('signup', TestsList.as_view(template_name="sign_up.html"), name='signup'),
]