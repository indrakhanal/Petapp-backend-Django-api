# Generated by Django 4.0.2 on 2022-04-16 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0012_rename_contact_no_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petdetailpost',
            name='user_contact',
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(max_length=40)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.animalcategory')),
            ],
        ),
    ]