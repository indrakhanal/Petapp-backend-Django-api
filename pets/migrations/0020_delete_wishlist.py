# Generated by Django 4.0.2 on 2022-04-21 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0019_alter_location_options_alter_municipality_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WishList',
        ),
    ]