from django.urls import path, re_path, register_converter
from django.utils.timezone import datetime
from rest_framework.urlpatterns import format_suffix_patterns

from daily_notes.views import (
    Index,
    GoalList,
    GoalDetail,
    DayDetail,
    SearchView
)

class DateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self,value):
        return datetime.strptime(value,"%Y-%m-%d")

    def to_url(self,value):
        return value.strftime("%Y-%m-%d")

class MonthConverter:
    regex = '[0-9]{4}-[0-9]{2}'

    def to_python(self, value:str):
        return value.split("-")

    def to_url(self, value:dict):
        return "{year}-{month}".format(**value)

register_converter(DateConverter, 'date')
register_converter(MonthConverter, 'month')

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('goals/<month:date>/' ,GoalList.as_view(), name='goal-list'),
    path('goals/id/<int:pk>/', GoalDetail.as_view(), name='goal-detail'),
    path('days/<date:date>/', DayDetail.as_view(), name='day-detail'),
    path('search/', SearchView.as_view(), name='search')
]

urlpatterns = format_suffix_patterns(urlpatterns)