# Generated by Django 2.0.5 on 2018-06-29 10:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data_display', '0008_auto_20180629_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='changes',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='changes',
            name='dateModified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='changes',
            name='userId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]