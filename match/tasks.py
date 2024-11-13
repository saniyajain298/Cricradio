from datetime import timedelta
from webbrowser import Error

from django.utils import timezone
from celery import shared_task, current_task
from celery.exceptions import MaxRetriesExceededError

from .scrapy import getLiveData


@shared_task(bind=True, max_retries=5, default_retry_delay=60)  # Retry configuration
def my_scheduled_task(self):
    from .scrapy import getMatchListScrappingJob
    from .utils import update_or_create_match

    try:
        start_time = timezone.now() + timedelta(minutes=1)
        end_condition = start_time + timedelta(minutes=10)

        if timezone.now() < end_condition:
            print("Executing scheduled task...", start_time, end_condition)

            # Get match data using your scraping job
            update_or_create_match()
            # Reschedule the task after 60 seconds
            my_scheduled_task.apply_async(countdown=120000000)

        else:
            print("Stop condition met, task will not retry.")

    except Exception as e:
        print(f"Error occurred: {e}")
        try:
            # Retry the task on failure, after a delay
            raise self.retry(exc=e)
        except MaxRetriesExceededError:
            print("Maximum retries exceeded.")


@shared_task
def call_match_api(match_unique_id):
    """
    Task to call the API for a match.
    This task is called when the match starts and every minute thereafter.
    """
    print("fvb", match_unique_id)
    try:
        print("yupppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        getLiveData(match_unique_id)
    except Error as e:
        print(f"Match with ID {match_unique_id} does not exist.", e)