# Generated by Django 4.1 on 2022-08-14 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='last_seen',
            field=models.DateTimeField(default=None),
        ),
    ]
