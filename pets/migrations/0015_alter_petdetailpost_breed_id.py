# Generated by Django 4.0.2 on 2022-04-17 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0014_petdetailpost_breed_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petdetailpost',
            name='breed_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pets.breed'),
        ),
    ]
