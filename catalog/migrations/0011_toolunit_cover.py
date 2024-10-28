# Generated by Django 5.1.1 on 2024-10-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_toolunit_tool_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolunit',
            name='cover',
            field=models.URLField(blank=True, help_text='URL for tool cover', null=True, verbose_name='cover_url'),
        ),
    ]
