# Generated by Django 3.1.3 on 2021-01-07 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210106_1051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name_plural': 'Feedback'},
        ),
        migrations.AlterModelOptions(
            name='urgentrequest',
            options={'verbose_name_plural': 'UrgentRequest'},
        ),
    ]
