# Generated by Django 4.0.2 on 2022-03-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_alter_location_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipality',
            name='municipality',
            field=models.CharField(max_length=100),
        ),
    ]
