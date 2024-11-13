from django.db import models

class Team(models.Model):
    team_unique_id = models.CharField(max_length=100, unique=True)
    team_name = models.CharField(max_length=255)

    def __str__(self):
        return self.team_unique_id


class Series(models.Model):
    unique_series_id = models.CharField(max_length=50, unique=True)
    series_name = models.CharField(max_length=255)
    host_team = models.ForeignKey(Team, to_field='team_unique_id', on_delete=models.CASCADE)
    type = models.IntegerField(default=0)
    status = models.CharField(max_length=100)
    month_year = models.CharField(max_length=20)
    tp = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.unique_series_id