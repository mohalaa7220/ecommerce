# Generated by Django 4.2.2 on 2023-07-16 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_remove_product_images_productimage_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images_url',
        ),
        migrations.AddField(
            model_name='productimage',
            name='image_url',
            field=models.URLField(blank=True, max_length=2220000, null=True),
        ),
    ]
