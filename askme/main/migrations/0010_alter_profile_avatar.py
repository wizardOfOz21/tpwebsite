# Generated by Django 4.2.2 on 2023-06-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_profile_profile_user_alter_answer_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.png', upload_to='avatars/%Y/%m/%d/'),
        ),
    ]
