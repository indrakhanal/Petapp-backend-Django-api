# Generated by Django 4.0.2 on 2022-04-17 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0017_alter_breed_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breed',
            name='breed',
            field=models.CharField(max_length=40),
        ),
    ]