# Generated by Django 5.0.6 on 2024-09-13 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0014_professorrating_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professorrating',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
