# Generated by Django 2.2.3 on 2019-10-29 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_appointment_instructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='lat',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='lon',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
