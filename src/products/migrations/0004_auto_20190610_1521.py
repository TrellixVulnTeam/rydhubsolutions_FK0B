# Generated by Django 2.2.1 on 2019-06-10 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190610_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='_supplier',
            new_name='product_supplier',
        ),
    ]
