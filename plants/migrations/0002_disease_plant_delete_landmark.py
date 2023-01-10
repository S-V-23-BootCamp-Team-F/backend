# Generated by Django 4.1.4 on 2023-01-10 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_code', models.CharField(max_length=10, verbose_name='질병 코드')),
                ('name', models.CharField(max_length=100, verbose_name='질병 이름')),
                ('cause', models.TextField(verbose_name='질병 원인')),
                ('feature', models.TextField(verbose_name='병진')),
                ('solution', models.TextField(verbose_name='방제 방법')),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10, verbose_name='식물 종류')),
                ('picture', models.URLField(max_length=250, verbose_name='식물 사진')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('disease_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plants.disease')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
        migrations.DeleteModel(
            name='Landmark',
        ),
    ]
