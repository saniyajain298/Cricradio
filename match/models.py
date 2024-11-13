from django.db import models

# Create your models here.

from django.db import models


class Match(models.Model):
    from common.models import Team, Series
    match_unique_id = models.CharField(max_length=100, null=True, blank=True, unique=True)  # Add `unique=True`

    match_date = models.DateField()
    # Define related_name for team1 and team2 to avoid clashes
    team1_unique_id = models.ForeignKey(Team, to_field='team_unique_id', on_delete=models.CASCADE,
                                        related_name='team1_matches', default=None)
    team2_unique_id = models.ForeignKey(Team, to_field='team_unique_id', on_delete=models.CASCADE,
                                        related_name='team2_matches', default=None)
    # Define related_name for host_team to avoid clashes
    host_team = models.ForeignKey(Team, to_field='team_unique_id', on_delete=models.CASCADE,
                                  related_name='host_matches', default=None)
    match_time = models.DateTimeField()
    series = models.ForeignKey(Series, to_field='unique_series_id', on_delete=models.CASCADE, default=1)
    status = models.IntegerField(null=True, blank=True)
    match_link = models.TextField(null=True, blank=True)
    start_time = models.BigIntegerField(null=True, blank=True)  # Start time in milliseconds
    end_time = models.BigIntegerField(null=True, blank=True)


    def __str__(self):
        return self.match_unique_id

class MatchData(models.Model):
    match_name = models.CharField(max_length=255, blank=True, null=True)
    match_id = models.ForeignKey('Match', to_field='match_unique_id', on_delete=models.CASCADE,
                                 related_name='match_data', default=None)
    balls_in_each_over = models.TextField(blank=True, null=True)
    bowling_status = models.CharField(max_length=255, blank=True, null=True)
    match_duration = models.IntegerField(blank=True, null=True)
    team_info = models.CharField(max_length=255, blank=True, null=True)
    match_ip_addresses = models.CharField(max_length=255, blank=True, null=True)
    run_rate = models.CharField(max_length=255, blank=True, null=True)
    match_ips_or_stats = models.TextField(blank=True, null=True)  # Consider using JSONField if it's structured data
    match_status = models.CharField(max_length=255, blank=True, null=True)
    player_performance_code = models.CharField(max_length=255, blank=True, null=True)
    player_score = models.IntegerField(blank=True, null=True)
    bowling_type = models.CharField(max_length=255, blank=True, null=True)
    event_code = models.IntegerField(blank=True, null=True)
    event_data = models.CharField(max_length=255, blank=True, null=True)
    match_code = models.CharField(max_length=255, blank=True, null=True)
    team_or_player_status = models.CharField(max_length=255, blank=True, null=True)
    match_score = models.CharField(max_length=255, blank=True, null=True)
    runs_in_current_over = models.CharField(max_length=255, blank=True, null=True)
    runs_required = models.CharField(max_length=255, blank=True, null=True)
    match_event_time = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Match Data: {self.match_name} ({self.match_id})"