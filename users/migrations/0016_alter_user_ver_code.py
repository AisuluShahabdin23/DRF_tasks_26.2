# Generated by Django 4.2.9 on 2024-01-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_user_ver_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ver_code',
            field=models.CharField(default='813291518738', max_length=15, verbose_name='Проверочный код'),
        ),
    ]