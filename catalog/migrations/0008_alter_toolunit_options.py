# Generated by Django 5.1.1 on 2024-10-17 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_merge_20241012_2341'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toolunit',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set tool as returned'),)},
        ),
    ]