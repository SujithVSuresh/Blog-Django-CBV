# Generated by Django 3.2.6 on 2021-09-20 10:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogmain', '0010_auto_20210919_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='following',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
