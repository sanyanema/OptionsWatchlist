# Generated by Django 3.1.2 on 2020-12-02 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201201_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='expiration_date',
            field=models.CharField(default='', max_length=200, unique=True),
        ),
    ]
