# Generated by Django 2.0.5 on 2018-06-20 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_display', '0003_auto_20180618_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
