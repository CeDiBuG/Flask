# Generated by Django 5.0.2 on 2024-02-08 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testform', '0005_remove_form_session_session_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='form',
        ),
        migrations.AddField(
            model_name='form',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='testform.session'),
            preserve_default=False,
        ),
    ]
