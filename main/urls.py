from django.urls import path

from .views import (home, ArticleList, ArticleDetail, MoodList, PhysicalActivityList,
                    TestsList, SearchResultsView, GratitudeJournalList, GratitudeJournalCreateView,
                    SlumberList, SlumberCreateView, show_profile, PhysicalCreateView, EmotionCreateView,
                    EmotionUpdateView, delete_emotion, CircleList, WaterList, DietList, HealthList)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),

    path('articles', ArticleList.as_view(template_name="article/articles_list.html"), name='articles'),
    path('articles/search', SearchResultsView.as_view(template_name="article/articles_list.html"),
         name='article_search'),
    path('article/<int:pk>/', ArticleDetail.as_view(template_name="article/article.html"), name='article'),

    path('moods', MoodList.as_view(template_name="trackers/mood.html"), name='moods'),
    path('moods/mood-editor', EmotionCreateView.as_view(template_name="trackers/mood-editor.html"), name='mood-editor'),
    path('moods/mood-editor/<int:pk>', EmotionUpdateView.as_view(template_name="trackers/mood-editor.html"), name='mood-edit'),
    path('moods/delete/<emotion_id>', delete_emotion, name='mood-delete'),

    path('water', WaterList.as_view(template_name="trackers/water.html"), name='water'),

    path('health', HealthList.as_view(template_name="trackers/health.html"), name="health"),

   path('diet', DietList.as_view(template_name="trackers/diet.html"), name='diet'),

    path('sleeping', SlumberList.as_view(template_name="trackers/sleeping_new.html"), name='sleeping'),
    path('sleeping/sleep-editor/', SlumberCreateView.as_view(template_name="trackers/sleep-editor.html"),
         name='sleep-editor'),


    path('activity', PhysicalActivityList.as_view(template_name="trackers/physical_activity.html"), name='activity'),
    path('activity/physical-editor', PhysicalCreateView.as_view(template_name="trackers/physical-editot.html"), name='activity-editor'),

    path('tests', TestsList.as_view(template_name="test/tests.html"), name='tests'),

    path('diary/text-editor', GratitudeJournalCreateView.as_view(template_name="diary/text_editor.html"),
         name='text-editor'),
    path('diary', GratitudeJournalList.as_view(template_name="diary/diary.html"), name='diary'),


    path('profile', show_profile, name='profile'),
    path('signin', TestsList.as_view(template_name="sign_in.html"), name='signin'),
    path('signup', TestsList.as_view(template_name="sign_up.html"), name='signup'),

    path('life-balance', CircleList.as_view(template_name="circle/circle.html"), name='circle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)