# Generated by Django 2.2.3 on 2019-10-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20191015_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('body', models.CharField(max_length=60)),
                ('data', models.CharField(max_length=60)),
            ],
        ),
    ]
