# Generated by Django 5.0.6 on 2024-09-20 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0021_alter_professor_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='department',
        ),
    ]
