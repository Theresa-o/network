# Generated by Django 4.0.2 on 2023-01-01 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]