# Generated by Django 4.0.2 on 2022-04-17 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0013_remove_petdetailpost_user_contact_breed'),
    ]

    operations = [
        migrations.AddField(
            model_name='petdetailpost',
            name='breed_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pets.breed'),
        ),
    ]
