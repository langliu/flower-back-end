# Generated by Django 2.0.5 on 2018-05-22 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_active_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(max_length=500, null=True),
        ),
    ]