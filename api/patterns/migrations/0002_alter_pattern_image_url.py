# Generated by Django 5.0 on 2024-03-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patterns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='image_url',
            field=models.URLField(unique=True),
        ),
    ]
