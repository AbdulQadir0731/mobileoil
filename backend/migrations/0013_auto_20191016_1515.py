# Generated by Django 2.2.3 on 2019-10-16 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_notifications_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='car',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
