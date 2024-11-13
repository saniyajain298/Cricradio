from django.apps import AppConfig

from .task import fetch_team_data_task, fetch_series_data_task


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):
        # Calling Celery tasks asynchronously using delay
        fetch_team_data_task.delay()
        fetch_series_data_task.delay()


