# Generated by Django 3.0.2 on 2021-01-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_delete_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Site_Info',
            },
        ),
    ]
