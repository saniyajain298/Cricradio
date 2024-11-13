# common/tasks.py
from celery import shared_task
from django.core.management import call_command

import logging

# Set up logging to log errors or info
logger = logging.getLogger(__name__)

@shared_task
def fetch_team_data_task():
    try:
        # Call the custom Django management command
        call_command('update_teams')

    except Exception as e:
        # Log the error if the command fails
        logger.error(f"Command failed: {str(e)}")
        raise
    except Exception as e:
        # Catch all other exceptions and log them
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise


@shared_task
def fetch_series_data_task():
    try:
        # Print to indicate task has started
        print('-----------------------------------------------------------')
        # Call the custom Django management command
        call_command('update_series')


    except Exception as e:
        # Log the error if the command fails
        logger.error(f"Command failed: {str(e)}")
        raise
    except Exception as e:
        # Catch all other exceptions and log them
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise
