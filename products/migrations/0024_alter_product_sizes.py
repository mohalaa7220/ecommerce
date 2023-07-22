# Generated by Django 4.2.2 on 2023-07-21 23:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_alter_productimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], max_length=20), size=None),
        ),
    ]
