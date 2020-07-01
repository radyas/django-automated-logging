# Generated by Django 3.0.7 on 2020-07-01 22:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('testmodels', '0003_auto_20180216_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExclusionText',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]