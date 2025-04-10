# Generated by Django 5.2 on 2025-04-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acme', '0011_machine_department_machine_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='model',
            field=models.CharField(default=None, help_text='Model Name for the machine', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machine',
            name='serial_number',
            field=models.CharField(default=None, help_text='Unique name or identifier for the machine', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
