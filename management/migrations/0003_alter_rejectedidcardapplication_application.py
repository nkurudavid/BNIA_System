# Generated by Django 4.2.4 on 2023-09-09 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_idcardregistration_citizen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rejectedidcardapplication',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rejected_application', to='management.idcardregistration', verbose_name='Application'),
        ),
    ]
