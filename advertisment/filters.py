from django_filters import FilterSet, DateFilter, Filter
from django import forms
from .models import Comment


class PostFilter(FilterSet):
    time_in = DateFilter(
        field_name='time_in',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Позже, чем',
        lookup_expr='date__gte',
    )

    class Meta:
        model = Comment
        fields = {
            'user': ['exact'],
            'time_in': [],
            'post': ['exact']
        }
