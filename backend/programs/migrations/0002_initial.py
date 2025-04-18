# Generated by Django 5.0.4 on 2025-04-18 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0001_initial'),
        ('subplans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readyprogram',
            name='subplan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subplans.subplan'),
        ),
        migrations.AddField(
            model_name='readyexercise',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='programs.readyprogram'),
        ),
    ]
