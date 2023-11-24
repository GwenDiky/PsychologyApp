
from django.contrib import admin
from django.urls import path, include
from main.views import MoodAPIUpdate, MoodViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'mood', MoodViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)), # http://127.0.0.1:8000/api/v1/mood
    # path('api/v1/moodlist', MoodViewSet.as_view({'get':'list'})),
    # path('api/v1/moodlist/<int:pk>/', MoodViewSet.as_view({'put':'update'})),
    path('', include('main.urls')),
]
