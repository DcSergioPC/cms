# Generated by Django 5.1 on 2024-10-04 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0005_article_author_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('publicado', 'Publicado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=10),
        ),
    ]
