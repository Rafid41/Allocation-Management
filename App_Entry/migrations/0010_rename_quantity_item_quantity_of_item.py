# Generated by Django 5.1.5 on 2025-02-16 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Entry', '0009_item_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='quantity',
            new_name='quantity_of_item',
        ),
    ]
