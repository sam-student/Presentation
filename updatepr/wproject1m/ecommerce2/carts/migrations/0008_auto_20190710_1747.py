# Generated by Django 2.1.3 on 2019-07-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_auto_20190710_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='product',
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
