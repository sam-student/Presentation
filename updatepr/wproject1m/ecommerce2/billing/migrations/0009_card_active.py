# Generated by Django 2.0 on 2019-07-07 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_delete_chargemanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
