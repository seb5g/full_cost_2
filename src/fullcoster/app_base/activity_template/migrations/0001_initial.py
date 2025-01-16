# Generated by Django 2.2.8 on 2019-12-20 09:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models

from full_cost.constants.activities import ActivityCategory
from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory
from fullcoster.constants.entities import ENTITIES

""" 

The template tag {{activity}} will be replaced by the name of the ActivityCategory enum specifying the Activity

"""

activity: Activity = ACTIVITIES[ActivityCategory[{{activity}}]]

activity_short_lower = f'{activity.activity_short.lower()}'


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lab', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment', models.CharField(max_length=200)),
                ('exp_type', models.CharField(choices=[(Activity.activity_short, Activity.activity_long)],
                                              default=Activity.activity_short, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('remark', models.TextField()),
                ('wu', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('billing', models.CharField(
                    choices=[(ent.short, ent.name) for ent in ENTITIES.values()],
                    default=list(ENTITIES.keys())[0], max_length=200)),
                ('nights', models.PositiveIntegerField(default=0)),
                ('date_from', models.DateField(default=django.utils.timezone.now)),
                ('date_to', models.DateField(default=django.utils.timezone.now)),
                ('time_from', models.SmallIntegerField(choices=[(0, 'Morning'), (1, 'Afternoon')], default=0)),
                ('time_to', models.SmallIntegerField(choices=[(0, 'Morning'), (1, 'Afternoon')], default=0)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to=f'{activity_short_lower}.Experiment')),
                ('extraction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 related_name=f'{activity_short_lower}_record_related',
                                                 related_query_name=f'{activity_short_lower}_records',
                                                 to='lab.Extraction')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name=f'{activity_short_lower}_record_related',
                                            related_query_name=f'{activity_short_lower}_records',
                                            to='lab.Group')),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name=f'{activity_short_lower}_record_related',
                                              related_query_name=f'{activity_short_lower}_records',
                                              to='lab.Project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name=f'{activity_short_lower}_record_related',
                                           related_query_name=f'{activity_short_lower}_records',
                                           to='lab.User')),
            ],
            options={
                'ordering': ['submitted'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalRecord',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('remark', models.TextField()),
                ('wu', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('billing', models.CharField(choices=[(ent.short, ent.name) for ent in ENTITIES.values()],
                                             default=list(ENTITIES.keys())[0], max_length=200)),
                ('nights', models.PositiveIntegerField(default=0)),
                ('date_from', models.DateField(default=django.utils.timezone.now)),
                ('date_to', models.DateField(default=django.utils.timezone.now)),
                ('time_from', models.SmallIntegerField(choices=[(0, 'Morning'), (1, 'Afternoon')], default=0)),
                ('time_to', models.SmallIntegerField(choices=[(0, 'Morning'), (1, 'Afternoon')], default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')],
                                                  max_length=1)),
                ('experiment', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                 on_delete=django.db.models.deletion.DO_NOTHING,
                                                 related_name='+', to=f'{activity_short_lower}.Experiment')),
                ('extraction', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                 on_delete=django.db.models.deletion.DO_NOTHING,
                                                 related_name='+', related_query_name=f'{activity_short_lower}_records',
                                                 to='lab.Extraction')),
                ('group', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                            on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                            related_query_name=f'{activity_short_lower}_records', to='lab.Group')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              related_query_name=f'{activity_short_lower}_records', to='lab.Project')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                           on_delete=django.db.models.deletion.DO_NOTHING,
                                           related_name='+', related_query_name=f'{activity_short_lower}_records',
                                           to='lab.User')),
            ],
            options={
                'verbose_name': 'historical record',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
