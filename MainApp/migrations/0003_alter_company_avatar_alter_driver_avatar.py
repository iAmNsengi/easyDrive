# Generated by Django 5.0.7 on 2024-07-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_alter_company_avatar_alter_company_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='avatar',
            field=models.ImageField(default='avatar.jpg', null='True', upload_to='company/'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='avatar',
            field=models.ImageField(default='avatar.jpg', null='True', upload_to='driver/'),
        ),
    ]
