# Generated by Django 5.1.7 on 2025-03-15 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
