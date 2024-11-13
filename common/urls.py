from django.urls import path
from .views import TeamListView

urlpatterns = [
    path('team/', TeamListView.as_view(), name='team'),
]