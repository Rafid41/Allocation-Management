# Generated by Django 5.1.5 on 2025-03-31 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Allocation', '0011_allocation_number_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_allocation',
            name='status',
            field=models.CharField(choices=[('Allocated', 'Allocated'), ('Cancelled', 'Cancelled')], default='Allocated', max_length=10),
        ),
    ]
