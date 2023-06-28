# Generated by Django 4.2.2 on 2023-06-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('time_zone', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=20)),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]