# Generated by Django 2.2.3 on 2019-10-21 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_notifications_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic',
            name='insurance',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mechanic',
            name='is_searching',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mechanic',
            name='license',
            field=models.CharField(default='555', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mechanic',
            name='license_image',
            field=models.ImageField(default='', max_length=160, upload_to='documents'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(max_length=160, upload_to='vehicles'),
        ),
    ]
