# Generated by Django 4.0 on 2024-08-29 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0004_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='users',
        ),
    ]
