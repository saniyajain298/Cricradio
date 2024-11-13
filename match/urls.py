from django.urls import path
from .views import MatchDataListView, MatchListView

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='matches'),
    path('matchdata/', MatchDataListView.as_view(), name='matchdata-list')
]