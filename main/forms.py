from django import forms
from .models import (Article, RecordGratitudeJournal, Slumber, PhysicalActivity, Emotion)


class SelectFormArticles(forms.ModelForm):
    category = forms.ChoiceField(
        label="Категория",
        choices=Article.THEMES,
        required=False,
        widget=forms.Select
    )

    class Meta:
        model = Article
        fields = ['category']

class GratitudeJournalForm(forms.ModelForm):
    class Meta:
        model = RecordGratitudeJournal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GratitudeJournalForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['to_whom'].widget.attrs.update({'class': 'form-control'})


class SlumberForm(forms.ModelForm):
    class Meta:
        model = Slumber
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SlumberForm, self).__init__(*args, **kwargs)
        self.fields['quality'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})


class PhysicalActivityForm(forms.ModelForm):
    class Meta:
        model = PhysicalActivity
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PhysicalActivityForm, self).__init__(*args, **kwargs)
        self.fields['average_pulse'].widget.attrs.update({'class': 'form-control'})
        self.fields['type_of_activity'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['intensity'].widget.attrs.update({'class': 'form-control'})
        self.fields['state_after'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})



class EmotionForm(forms.ModelForm):
    class Meta:
        model = Emotion
        exclude = ("author",)

    def __init__(self, *args, **kwargs):
        super(EmotionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['effort'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['reason'].widget.attrs.update({'class': 'form-control'})


class MonthSelectForm(forms.Form):
    month = forms.IntegerField(
        label='Месяц',
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер месяца'})
    )
