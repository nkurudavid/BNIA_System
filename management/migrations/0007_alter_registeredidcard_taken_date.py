# Generated by Django 4.2.5 on 2023-09-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_nidcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredidcard',
            name='taken_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date taken'),
        ),
    ]
