# Generated by Django 5.0.4 on 2025-04-18 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='trainerstudentprogram',
            name='student',
            field=models.ForeignKey(limit_choices_to={'is_trainer': False}, on_delete=django.db.models.deletion.CASCADE, related_name='student_programs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='trainerstudentprogram',
            name='trainer',
            field=models.ForeignKey(limit_choices_to={'is_trainer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_programs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exercise',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='programs.trainerstudentprogram'),
        ),
    ]
