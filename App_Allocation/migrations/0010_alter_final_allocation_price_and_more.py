# Generated by Django 5.1.5 on 2025-03-14 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Allocation', '0009_alter_allocation_number_allocation_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='final_allocation',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='temporary_allocation',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
