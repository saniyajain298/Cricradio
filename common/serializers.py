from rest_framework import serializers
from .models import Team, Series


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_unique_id', 'team_name']


class SeriesSerializer(serializers.ModelSerializer):

    host_team = TeamSerializer(read_only=True)

    class Meta:
        model = Series
        fields = ['unique_series_id', 'series_name', 'host_team', 'type', 'status', 'month_year', 'tp']