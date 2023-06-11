# Generated by Django 4.2.2 on 2023-06-11 17:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import dsbd.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='取得開始時刻')),
                ('start_at', models.DateTimeField(blank=True, null=True, verbose_name='サービス開始日')),
                ('end_at', models.DateTimeField(blank=True, null=True, verbose_name='サービス終了日')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効')),
                ('type1', models.CharField(choices=[('Wireguardによる接続', 'Wireguardによる接続'), ('その他', 'その他')], max_length=200, verbose_name='type1')),
                ('content', dsbd.models.MediumTextField(blank=True, default='', verbose_name='内容')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='custom_auth.customgroup')),
            ],
        ),
    ]
