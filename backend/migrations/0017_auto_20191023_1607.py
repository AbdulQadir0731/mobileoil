# Generated by Django 2.2.3 on 2019-10-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20191021_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='grade',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
