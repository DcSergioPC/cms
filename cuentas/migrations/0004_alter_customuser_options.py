# Generated by Django 4.0 on 2024-08-29 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0003_alter_customuser_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'usuarios'},
        ),
    ]