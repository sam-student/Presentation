# Generated by Django 2.0 on 2019-05-31 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectviewed',
            name='product',
        ),
    ]
