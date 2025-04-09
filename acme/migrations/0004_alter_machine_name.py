# Generated by Django 5.2 on 2025-04-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acme', '0003_machine_ticket_category_alter_ticket_attachment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='name',
            field=models.CharField(help_text='Unique name or identifier for the machine', max_length=100, unique=True),
        ),
    ]
