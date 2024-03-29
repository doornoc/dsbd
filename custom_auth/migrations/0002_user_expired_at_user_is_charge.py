# Generated by Django 4.2.2 on 2023-07-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expired_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='有効期限'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_charge',
            field=models.BooleanField(default=False, verbose_name='課金'),
        ),
    ]
