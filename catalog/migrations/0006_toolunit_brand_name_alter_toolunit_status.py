# Generated by Django 5.1.1 on 2024-10-12 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_toolunit_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolunit',
            name='brand_name',
            field=models.CharField(blank=True, help_text='Enter arand name', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='toolunit',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'На обслуживании'), ('o', 'В аренде'), ('a', 'Доступен'), ('r', 'Зарезервирован')], default='m', help_text='Tool availability', max_length=1),
        ),
    ]
