# Generated by Django 2.2.13 on 2021-01-28 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]