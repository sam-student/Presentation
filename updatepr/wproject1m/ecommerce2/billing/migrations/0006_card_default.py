# Generated by Django 2.0 on 2019-06-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]