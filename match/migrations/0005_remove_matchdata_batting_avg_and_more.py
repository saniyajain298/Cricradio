# Generated by Django 5.1.3 on 2024-11-13 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_remove_match_w'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchdata',
            name='batting_avg',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='batting_code',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='fielding_position',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='final_score',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='match_code_event',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='match_progress',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='match_status_details',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='next_event_time',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='play_code',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='player_code',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='player_performance',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='player_score_status',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='query_status',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='special_match_code',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='team_code',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='team_or_player_status_details',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='team_status',
        ),
    ]
