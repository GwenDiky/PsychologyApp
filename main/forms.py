from django import forms
from .models import Article, RecordGratitudeJournal, Slumber


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


