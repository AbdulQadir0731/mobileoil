# Generated by Django 2.2.3 on 2019-10-14 11:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20191009_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.CharField(default='oil', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='zip_code',
            field=models.CharField(default=0, max_length=60),
            preserve_default=False,
        ),
    ]
