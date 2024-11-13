from django.shortcuts import render
from rest_framework import generics

from .models import Team
from .serializers import TeamSerializer


# Create your views here.
class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()  # Query all teams from the Team model
    serializer_class = TeamSerializer  # Use the TeamSerializer to serialize the queryset

    # Optional: If you want to filter the teams based on some parameters, you can add a filter method
    def get_queryset(self):
        queryset = Team.objects.all()  # Get all teams

        # Example filtering logic (you can modify this based on your requirements)
        team_name = self.request.query_params.get('name', None)
        if team_name:
            queryset = queryset.filter(name__icontains=team_name)

        # Add more filters if necessary (e.g., filtering by location, category, etc.)

        return queryset