# Generated by Django 4.0.2 on 2022-04-19 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pets', '0018_alter_breed_breed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('district',), 'verbose_name_plural': 'Locations'},
        ),
        migrations.AlterModelOptions(
            name='municipality',
            options={'ordering': ('municipality',)},
        ),
        migrations.RenameField(
            model_name='wishlistitem',
            old_name='pets',
            new_name='post_id',
        ),
        migrations.RemoveField(
            model_name='wishlistitem',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wish_list_items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]