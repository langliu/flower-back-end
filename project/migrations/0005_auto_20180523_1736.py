# Generated by Django 2.0.5 on 2018-05-23 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20180516_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdetail',
            name='complete_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='complete_time',
            field=models.DateTimeField(null=True),
        ),
    ]
