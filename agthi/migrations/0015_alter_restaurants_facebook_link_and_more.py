# Generated by Django 5.0.8 on 2024-08-12 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agthi', '0014_alter_restaurants_facebook_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurants',
            name='facebook_link',
            field=models.URLField(default='https://www.facebook.com/'),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='instagram_link',
            field=models.URLField(default='https://www.instagram.com/'),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='twitter_link',
            field=models.URLField(default='https://www.twitter.com/'),
        ),
    ]
