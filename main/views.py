from django.forms import model_to_dict
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from rest_framework import generics, viewsets
from rest_framework.decorators import action

from .models import Mood, Article
from .serializers import MoodSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# class MoodApiView(generics.ListAPIView):
#     queryset = Mood.objects.all()
#     serializer_class = MoodSerializer

# class MoodAPIList(generics.ListCreateAPIView):
#     queryset = Mood.objects.all() # Ленивый запрос. Ленивый запрос выполняется только в тот момент, когда нужны данные, а жадные сразу
#     serializer_class = MoodSerializer
#
#
class MoodAPIUpdate(generics.UpdateAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer

    @action(methods=['get'], detail=False)
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats':[c.name ]})


# class MoodAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Mood.objects.all()
#     serializer_class = MoodSerializer

class MoodViewSet(viewsets.ModelViewSet):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer

# class MoodApiView(APIView):
#     def get(self, request):
#         queryset = Mood.objects.all().values()
#         return Response({
#             'posts':MoodSerializer(queryset, many=True).data
#         })
#
#     def post(self, request):
#
#         # проверяем корректность
#         serializer = MoodSerializer(data = request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save() # вызывается create() MoodSerializer
#
#         return Response({'post':serializer.data}) # коллекция data представляет собой словарь
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error":"Method put not allowed"})
#         try:
#             instance = Mood.objects.get(pk = pk)
#         except:
#             return Response({"error":"Object does not exist"})
#
#         serializer = MoodSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save() # вызывает метод update(), тк параметры MoodSerializer data и instance
#         return Response({"post":serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error":"Method DELETE not allowed"})
#
#         try:
#             instance = Mood.objects.get(pk = pk)
#         except:
#             return Response({"error":"Object does not exist"})
#
#         instance.delete()
#         return Response({"post":"delete post " + str(pk)})
#

def home(request):
    # with open('templates/main.html', 'r', encoding='utf-8') as file:
    #     content = file.read()

    return render(request, 'main/main.html', {})


class ArticleDetail(DetailView):
    template = "article.html"


class ArticleList(ListView):
    model = Article
    context_object_name = "articles"

class MoodList(ListView):
    model = Mood
    context_object_name = "moods"

class SleepList(ListView):
    model = Mood
    context_object_name = "moods"

class PhysicalActivityList(ListView):
    model = Mood
    context_object_name = "moods"


class Entry(ListView):
    model = Mood
    context_object_name = "moods"


class TestsList(ListView):
    model = Mood
    context_object_name = "moods"