# Generated by Django 4.2.9 on 2024-01-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='Slug продукта'),
        ),
    ]
