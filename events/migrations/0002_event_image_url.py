# Generated by Django 4.2.5 on 2023-09-23 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]