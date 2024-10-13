# Generated by Django 5.1.1 on 2024-10-12 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_toolunit_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='brand_name',
        ),
        migrations.AddField(
            model_name='toolunit',
            name='brand_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.brand'),
        ),
        migrations.AlterField(
            model_name='toolunit',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'На обслуживании'), ('o', 'В аренде'), ('a', 'Доступен'), ('r', 'Зарезервирован')], default='m', help_text='Tool availability', max_length=1),
        ),
    ]