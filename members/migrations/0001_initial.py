# Generated by Django 4.1.4 on 2023-01-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, verbose_name='사용자 이메일')),
                ('user_status', models.BooleanField(default=True, verbose_name='사용자 상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='사용자 생성일')),
            ],
        ),
    ]