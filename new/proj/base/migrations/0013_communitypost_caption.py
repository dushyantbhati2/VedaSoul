# Generated by Django 4.2.5 on 2024-01-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_communityuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitypost',
            name='caption',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]