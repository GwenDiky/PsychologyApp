from django.db.models import Q
from collections import defaultdict
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from datetime import datetime, timedelta
from rest_framework import generics, viewsets
from rest_framework.decorators import action
import itertools
import calendar
from .forms import SelectFormArticles, GratitudeJournalForm
from .models import Mood, Article, RecordGratitudeJournal, Slumber
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

    # @action(methods=['get'], detail=False)
    # def category(self, request):
    #     cats = Category.objects.all()
    #     return Response({'cats':[c.name ]})


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

class ArticleList(ListView):
    model = Article
    context_object_name = "object_list"
    paginate_by = 5
    form_class = SelectFormArticles

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)

        if self.request.method == 'GET' and form.is_valid():
            selected_category = form.cleaned_data.get('category')
            if selected_category:
                queryset = queryset.filter(category=selected_category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class SearchResultsView(ListView):
    model = Article
    def get_queryset(self):
        query = self.request.GET.get("title")
        if query:
            object_list = Article.objects.filter(
                Q(title__icontains=query)
            )
            return object_list
        else:
            return Article.objects.all()


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'


class GratitudeJournalList(ListView):
    model = RecordGratitudeJournal
    context_object_name = 'records'

    paginate_by = 2
    def get_queryset(self):
        return RecordGratitudeJournal.objects.filter(author=self.request.user)

class GratitudeJournalCreateView(CreateView):
    model = RecordGratitudeJournal
    form_class = GratitudeJournalForm
    success_url = reverse_lazy("main:home")

class SlumberList(ListView):
    model = Slumber
    context_object_name = 'sleeping'
    def get_queryset(self):
        current_month = datetime.today().month  # get the current month
        query_set = Slumber.objects.filter(author=self.request.user,
                                           date__month=current_month)  # get records of the current user

        d = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'Sunday': []
        }

        # Определение первого дня месяца
        first_day_of_month = datetime(datetime.today().year, current_month, 1)

        # Определение последнего дня месяца
        last_day_of_month = datetime(datetime.today().year, current_month % 12 + 1, 1) - timedelta(days=1)

        # Заполнение данными из query_set
        for day in query_set:
            day_of_week = day.date.strftime('%A')
            d[day_of_week].append(day)


        numberOfDays = calendar.monthrange(datetime.today().year, current_month)[1] # кол-во месяцев в текущем месяце
        first_day_of_the_week = first_day_of_month.strftime('%A')

        # определяем какие дни заняты
        filed_out_days = []
        for day in query_set:
            filed_out_days.append(day.date.day)


        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days.index(first_day_of_the_week)
        size = 7 # т.к. в неделе 7 дней

        for i in range(1, numberOfDays + 1):  # итерация по каждому дню месяца
            if i in filed_out_days: # занята ли дата экземпляром Slumber
                current_index += 1
                if current_index == size:
                    current_index = 0
                continue
            d[days[current_index]].append(i)  # Добавляет день  в список для дня недели
            current_index += 1
            if current_index == size:
                current_index = 0

        # Сортировка
        for day_of_week, values in d.items():
            def custom_sort(val):
                if isinstance(val, Slumber):
                    return val.date.day
                return val
            d[day_of_week].sort(key=custom_sort)

        return d


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