# Generated by Django 4.2.2 on 2023-07-22 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_alter_product_sizes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(related_name='product_sizes', to='products.sizes'),
        ),
    ]
