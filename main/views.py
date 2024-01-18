from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from datetime import datetime, timedelta
import calendar

from rest_framework import generics

from .forms import SelectFormArticles, GratitudeJournalForm, SlumberForm, PhysicalActivityForm, EmotionForm
from .models import Article, RecordGratitudeJournal, Slumber, Emotion, PhysicalActivity
from collections import Counter

def home(request):
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
    success_url = reverse_lazy("main:diary")


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

        numberOfDays = calendar.monthrange(datetime.today().year, current_month)[1]  # кол-во месяцев в текущем месяце
        first_day_of_the_week = first_day_of_month.strftime('%A')

        # определяем какие дни заняты
        filed_out_days = []
        for day in query_set:
            filed_out_days.append(day.date.day)

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days.index(first_day_of_the_week)
        size = 7  # т.к. в неделе 7 дней

        for i in range(1, numberOfDays + 1):  # итерация по каждому дню месяца
            if i in filed_out_days:  # занята ли дата экземпляром Slumber
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

        # Добавляем пропуски первым элементом списка, если день в месяце не первый. Добавляем до того момента, пока не найдем первый день
        """
        Итог:
            1 2 3
        6 7 8 9 10
        """

        if 1 not in d['Monday']:
            d['Monday'].insert(0, '-')
            if 1 not in d['Tuesday']:
                d['Tuesday'].insert(0, '-')
                if 1 not in d['Wednesday']:
                    d['Wednesday'].insert(0, '-')
                    if 1 not in d['Thursday']:
                        d['Thursday'].insert(0, '-')
                        if 1 not in d['Friday']:
                            d['Friday'].insert(0, '-')
                            if 1 not in d['Saturday']:
                                d['Saturday'].insert(0, '-')
                                if 1 not in d['Sunday']:
                                    d['Sunday'].insert(0, '-')

        if d['Sunday'][0] == "-":
            for k in d.keys():
                d[k].pop(0)


        return d

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        current_month = datetime.today().month  # get the current month
        query_set = Slumber.objects.filter(author=self.request.user,
                                           date__month=current_month)

        count_of_sleeping_in_month = 0
        count_of_quality_in_month = 0

        for day in query_set:
            count_of_sleeping_in_month += day.duration
            count_of_quality_in_month += day.quality

        if count_of_sleeping_in_month:
            data['average_slumber'] = round(count_of_sleeping_in_month / len(query_set), 1)
        if count_of_quality_in_month:
            data['average_quality'] = round(count_of_quality_in_month / len(query_set), 1)

        return data


class SlumberCreateView(CreateView):
    model = Slumber
    form_class = SlumberForm
    success_url = reverse_lazy("main:sleeping")


class MoodList(ListView):
    model = Emotion
    context_object_name = "moods"

    def get_queryset(self, current_month=datetime.today().month):
        query_set = (Emotion.objects.select_related("author")
                     .filter(author=self.request.user,
                             date__month=current_month))

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

        numberOfDays = calendar.monthrange(datetime.today().year, current_month)[1]  # кол-во месяцев в текущем месяце
        first_day_of_the_week = first_day_of_month.strftime('%A')

        # определяем какие дни заняты
        filed_out_days = []
        for day in query_set:
            filed_out_days.append(day.date.day)

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days.index(first_day_of_the_week)
        size = 7  # т.к. в неделе 7 дней

        for i in range(1, numberOfDays + 1):  # итерация по каждому дню месяца
            if i in filed_out_days:  # занята ли дата экземпляром Slumber
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
                if isinstance(val, Emotion):
                    return val.date.day
                return val

            d[day_of_week].sort(key=custom_sort)

        # Добавляем пропуски первым элементом списка, если день в месяце не первый. Добавляем до того момента, пока не найдем первый день
        """
        Итог:
            1 2 3
        6 7 8 9 10
        """
        if 1 not in d['Monday']:
            d['Monday'].insert(0, '-')
            if 1 not in d['Tuesday']:
                d['Tuesday'].insert(0, '-')
                if 1 not in d['Wednesday']:
                    d['Wednesday'].insert(0, '-')
                    if 1 not in d['Thursday']:
                        d['Thursday'].insert(0, '-')
                        if 1 not in d['Friday']:
                            d['Friday'].insert(0, '-')
                            if 1 not in d['Saturday']:
                                d['Saturday'].insert(0, '-')
                                if 1 not in d['Sunday']:
                                    d['Sunday'].insert(0, '-')

        if d['Sunday'][0] == "-":
            for k in d.keys():
                d[k].pop(0)

        return d

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        current_month = datetime.today().month  # get the current month
        query_set = Emotion.objects.filter(author=self.request.user,
                                           date__month=current_month)

        count_average_effort = 0

        for day in query_set:
            count_average_effort += day.effort

        if count_average_effort:
            data['average_effort'] = round(count_average_effort / len(query_set), 1)

        emotions_counter = Counter(Emotion.objects.values_list("title", flat=True))
        data['the_most_common_emotion'] = emotions_counter.most_common(1)[0][0]

        return data


class PhysicalActivityList(ListView):
    model = PhysicalActivity
    context_object_name = "activities"

    def get_queryset(self):
        current_month = datetime.today().month
        query_set = PhysicalActivity.objects.filter(author=self.request.user,
                                                    date__month=current_month)

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

        numberOfDays = calendar.monthrange(datetime.today().year, current_month)[1]  # кол-во месяцев в текущем месяце
        first_day_of_the_week = first_day_of_month.strftime('%A')

        # определяем какие дни заняты
        filed_out_days = []
        for day in query_set:
            filed_out_days.append(day.date.day)

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days.index(first_day_of_the_week)
        size = 7  # т.к. в неделе 7 дней

        for i in range(1, numberOfDays + 1):  # итерация по каждому дню месяца
            if i in filed_out_days:  # занята ли дата экземпляром Slumber
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
                if isinstance(val, PhysicalActivity):
                    return val.date.day
                return val

            d[day_of_week].sort(key=custom_sort)

        # Добавляем пропуски первым элементом списка, если день в месяце не первый. Добавляем до того момента, пока не найдем первый день
        """
        Итог:
            1 2 3
        6 7 8 9 10
        """

        if 1 not in d['Monday']:
            d['Monday'].insert(0, '-')
            if 1 not in d['Tuesday']:
                d['Tuesday'].insert(0, '-')
                if 1 not in d['Wednesday']:
                    d['Wednesday'].insert(0, '-')
                    if 1 not in d['Thursday']:
                        d['Thursday'].insert(0, '-')
                        if 1 not in d['Friday']:
                            d['Friday'].insert(0, '-')
                            if 1 not in d['Saturday']:
                                d['Saturday'].insert(0, '-')
                                if 1 not in d['Sunday']:
                                    d['Sunday'].insert(0, '-')

        if d['Sunday'][0] == "-":
            for k in d.keys():
                d[k].pop(0)


        return d

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        current_month = datetime.today().month  # get the current month
        query_set = PhysicalActivity.objects.filter(author=self.request.user,
                                                    date__month=current_month)

        count_average_pulse = 0
        count_of_duration_in_month = 0

        for day in query_set:
            count_average_pulse += day.average_pulse
            count_of_duration_in_month += day.duration

        if count_average_pulse:
            data['average_pulse_month'] = round(count_average_pulse / len(query_set), 1)

        if count_of_duration_in_month != 0:
            data['average_duration'] = int(count_of_duration_in_month / 31)

        return data


class PhysicalCreateView(CreateView, UpdateView):
    model = PhysicalActivity
    form_class = PhysicalActivityForm
    success_url = reverse_lazy("main:activity")


class EmotionCreateView(CreateView):
    model = Emotion
    form_class = EmotionForm
    success_url = reverse_lazy("main:moods")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EmotionDeleteView(DeleteView):
    model = Emotion
    success_url = reverse_lazy("main:moods")


class EmotionUpdateView(UpdateView):
    model = Emotion
    fields = ['title', 'effort', 'date', 'reason']
    success_url = reverse_lazy("main:moods")


class TestsList(ListView):
    model = Emotion
    context_object_name = "moods"


def show_profile(request):
    username = request.user.username
    return render(request, 'profile.html', {'username': username})
