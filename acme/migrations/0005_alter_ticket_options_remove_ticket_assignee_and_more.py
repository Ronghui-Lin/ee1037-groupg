# Generated by Django 5.2 on 2025-04-08 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acme', '0004_alter_machine_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='attachment',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='category',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='reporter',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='resolved_at',
        ),
        migrations.AddField(
            model_name='ticket',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_tickets', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Open', 'Open'), ('In Progress', 'In Progress'), ('Pending Customer', 'Pending Customer'), ('Closed', 'Closed')], default='New', max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='subject',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='TicketAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='ticket_attachments/')),
                ('filename', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='acme.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='acme.ticket')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
