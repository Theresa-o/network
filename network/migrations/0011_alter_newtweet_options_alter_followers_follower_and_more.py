# Generated by Django 4.0.2 on 2023-01-15 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_followers_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newtweet',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='followers',
            name='follower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='targets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followers',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
