# Generated by Django 5.0.6 on 2024-09-20 08:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0023_professor_department'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='professor',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='professors', to='ratings.department'),
            preserve_default=False,
        ),
    ]
