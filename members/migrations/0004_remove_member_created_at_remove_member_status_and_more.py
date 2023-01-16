# Generated by Django 4.1.4 on 2023-01-16 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_member_options_alter_member_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='member',
            name='status',
        ),
        migrations.RemoveField(
            model_name='member',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='member',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
