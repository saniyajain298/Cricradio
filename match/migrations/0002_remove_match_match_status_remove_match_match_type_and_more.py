# Generated by Django 5.1.3 on 2024-11-13 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_series_tp_alter_series_type'),
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='match_status',
        ),
        migrations.RemoveField(
            model_name='match',
            name='match_type',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winning_team',
        ),
        migrations.AddField(
            model_name='match',
            name='end_time',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='host_team',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='host_matches', to='common.team', to_field='team_unique_id'),
        ),
        migrations.AddField(
            model_name='match',
            name='match_unique_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='series',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.series', to_field='unique_series_id'),
        ),
        migrations.AddField(
            model_name='match',
            name='start_time',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='team1_unique_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team1_matches', to='common.team', to_field='team_unique_id'),
        ),
        migrations.AddField(
            model_name='match',
            name='team2_unique_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team2_matches', to='common.team', to_field='team_unique_id'),
        ),
        migrations.AddField(
            model_name='match',
            name='w',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_time',
            field=models.DateTimeField(),
        ),
    ]
