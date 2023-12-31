# Generated by Django 4.2.4 on 2023-09-09 17:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')], default='', max_length=10, verbose_name='Gender')),
                ('volume_number', models.CharField(max_length=50, unique=True, verbose_name='Volume Number')),
                ('nid_number', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='NID Card Number')),
                ('birthdate', models.DateField(verbose_name='Birthdate')),
                ('createdDate', models.DateField(auto_now_add=True, verbose_name='Created Date')),
            ],
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commune_name', models.CharField(max_length=50, verbose_name='Commune Name')),
            ],
        ),
        migrations.CreateModel(
            name='IDCardRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='Email Address')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='registration/citizen/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Citizen Image')),
                ('status', models.CharField(choices=[('', 'Select Status'), ('Waiting', 'Waiting'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Waiting', max_length=20, verbose_name='Status')),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Registration Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.citizen', verbose_name='Citizen')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('resident_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrations', to='management.commune', verbose_name='Resident Address')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_name', models.CharField(max_length=50, unique=True, verbose_name='Province Name')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100, unique=True, verbose_name='Service Title')),
                ('requirements', models.TextField(verbose_name='Requirements')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RejectedIDCardApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejected_reason', models.CharField(choices=[('', 'Select Reason to reject'), ('Bad Picture', 'Bad Picture')], default='Bad Picture', max_length=20, verbose_name='Why rejected')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.idcardregistration', verbose_name='Application')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredIDCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=20, verbose_name='ID Number')),
                ('takenCount', models.CharField(choices=[('', 'Select Parent'), ('First', 'First'), ('Second', 'Second'), ('Third', 'Third')], default='', max_length=10, verbose_name='Taken Count')),
                ('is_taken', models.BooleanField(default=False, verbose_name='Is taken?')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Date created')),
                ('taken_date', models.DateField(verbose_name='Date taken')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.citizen', verbose_name='Citizen')),
                ('placeofissue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registerd_idcard', to='management.commune', verbose_name='Place of Issue')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('files', models.FileField(upload_to='publications/', verbose_name='File')),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LostIDCardReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=20, verbose_name='Lost Card ID number')),
                ('date_lost', models.DateField(verbose_name='When lost')),
                ('description', models.TextField(verbose_name='Description')),
                ('email', models.EmailField(max_length=255, verbose_name='Email Address')),
                ('contact_info', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Contact Info')),
                ('status', models.CharField(choices=[('', 'Select Status'), ('Waiting', 'Waiting'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='', max_length=20, verbose_name='Status')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lost_reports', to='management.citizen', verbose_name='Citizen')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commune',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communes', to='management.province', verbose_name='Province'),
        ),
        migrations.CreateModel(
            name='Colline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colline_name', models.CharField(max_length=50, verbose_name='Colline Name')),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collines', to='management.commune', verbose_name='Commune')),
            ],
        ),
        migrations.CreateModel(
            name='CitizenParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(choices=[('', 'Select Parent'), ('Father', 'Father'), ('Mother', 'Mother')], default='', max_length=10, verbose_name='Parent')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Last Name')),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='management.citizen', verbose_name='Citizen')),
            ],
        ),
        migrations.AddField(
            model_name='citizen',
            name='birth_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.colline', verbose_name='Resident Address'),
        ),
        migrations.AddField(
            model_name='citizen',
            name='recorded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
