from rest_framework import serializers
from .models import Match, MatchData
from common.models import Team, Series

class MatchSerializer(serializers.ModelSerializer):
    team1_unique_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    team2_unique_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    host_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    series = serializers.PrimaryKeyRelatedField(queryset=Series.objects.all())

    class Meta:
        model = Match
        fields = [
            'match_unique_id',
            'match_date',
            'team1_unique_id',
            'team2_unique_id',
            'host_team',
            'match_time',
            'series',
            'status',
            'match_link',
            'start_time',
            'end_time'
        ]

class MatchDataSerializer(serializers.ModelSerializer):
    match_id = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())

    class Meta:
        model = MatchData
        fields = [
            'match_name',
            'match_id',
            'balls_in_each_over',
            'bowling_status',
            'match_duration',
            'team_info',
            'match_ip_addresses',
            'run_rate',
            'match_ips_or_stats',
            'match_status',
            'player_performance_code',
            'player_score',
            'bowling_type',
            'event_code',
            'event_data',
            'match_code',
            'team_or_player_status',
            'match_score',
            'runs_in_current_over',
            'runs_required',
            'match_event_time'
        ]
