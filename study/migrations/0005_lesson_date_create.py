# Generated by Django 4.2.9 on 2024-01-13 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0004_alter_subscription_course_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='date_create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата выхода урока'),
            preserve_default=False,
        ),
    ]