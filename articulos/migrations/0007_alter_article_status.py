# Generated by Django 5.1 on 2024-10-05 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0006_alter_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('revision', 'Revision'), ('aprobado', 'Aprobado'), ('publicado', 'Publicado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=10),
        ),
    ]
