# Generated by Django 5.1 on 2024-10-17 08:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('details', models.TextField()),
                ('image', models.ImageField(upload_to='events/')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]