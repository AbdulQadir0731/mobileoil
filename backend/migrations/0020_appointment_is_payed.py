# Generated by Django 2.2.3 on 2019-10-25 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_user_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_payed',
            field=models.BooleanField(default=False),
        ),
    ]
