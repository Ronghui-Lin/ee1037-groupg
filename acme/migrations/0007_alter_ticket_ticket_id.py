# Generated by Django 5.2 on 2025-04-09 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acme', '0006_ticket_ticket_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_id',
            field=models.CharField(blank=True, default=None, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
