# Generated by Django 5.1.5 on 2025-03-05 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Allocation', '0003_final_allocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporary_allocation',
            name='item_primary_key',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
