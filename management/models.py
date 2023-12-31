from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField



# Create your models here.
class Province(models.Model):
    province_name = models.CharField(verbose_name="Province Name", max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.province_name


class Commune(models.Model):
    province = models.ForeignKey(Province, verbose_name="Province", related_name="communes", on_delete=models.CASCADE)
    commune_name = models.CharField(verbose_name="Commune Name", max_length=50, blank=False)

    def __str__(self):
        return self.commune_name


class Colline(models.Model):
    commune = models.ForeignKey(Commune, verbose_name="Commune", related_name="collines", on_delete=models.CASCADE)
    colline_name = models.CharField(verbose_name="Colline Name", max_length=50, blank=False)

    def __str__(self):
        return self.colline_name



class Citizen(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    birth_place = models.ForeignKey(Colline, verbose_name="Resident Address", on_delete=models.SET_NULL, blank=True, null=True)
    volume_number = models.CharField(verbose_name="Volume Number", max_length=50, unique=True, blank=False, null=False)
    nid_number = models.CharField(verbose_name="NID Card Number", max_length=50, unique=True, blank=True, null=True)
    birthdate = models.DateField(verbose_name="Birthdate", blank=False)
    picture = models.ImageField(
        verbose_name="Citizen Image",
        upload_to="citizen/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    createdDate = models.DateField(verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class NIDCard(models.Model):
    citizen = models.OneToOneField(Citizen, verbose_name="NID Card", related_name="nid_card", on_delete=models.CASCADE)
    qr_code_image = models.ImageField(upload_to='citizen/nid_card_qr_codes/')
    date = models.DateField(verbose_name="Generated Date", auto_now_add=True)

    def __str__(self):
        return f'NID Card - {self.citizen.nid_number}'


class CitizenParent(models.Model):
    class Parent(models.TextChoices):
        SELECT = "", "Select Parent"
        FATHER = "Father", "Father"
        MOTHER = "Mother", "Mother"

    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", related_name="parents", on_delete=models.CASCADE)
    parent = models.CharField(verbose_name="Parent", choices=Parent.choices, default=Parent.SELECT, max_length=10)
    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=True)

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)


class IDCardRegistration(models.Model):
    class Status(models.TextChoices):
        SELECT = "", "Select Status"
        WAITING = "Waiting", "Waiting"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", related_name="id_registrations", on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Email Address", max_length=255, blank=False)
    resident_address = models.ForeignKey(Commune, verbose_name="Resident Address", related_name="registrations", on_delete=models.SET_NULL, blank=True, null=True)
    picture = models.ImageField(
        verbose_name="Citizen Image",
        upload_to="registration/citizen/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    status = models.CharField(verbose_name="Status", choices=Status.choices, default=Status.WAITING, max_length=20)
    registration_date = models.DateField(verbose_name="Registration Date", auto_now_add=True)

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.picture))

    image.allow_tags = True

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)



class RegisteredIDCard(models.Model):
    
    class TakenCount(models.TextChoices):
        SELECT = "", "Select Parent"
        FIRST = "First", "First"
        SECOND = "Second", "Second"
        THIRD = "Third", "Third"
    
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", on_delete=models.CASCADE)
    card_number = models.CharField(verbose_name="ID Number", max_length=20)
    takenCount = models.CharField(verbose_name="Taken Count", choices=TakenCount.choices, default=TakenCount.SELECT, max_length=10)
    is_taken = models.BooleanField(verbose_name="Is taken?", default=False)
    placeofissue = models.ForeignKey(Commune, verbose_name="Place of Issue", related_name="registerd_idcard", on_delete=models.SET_NULL, blank=True, null=True)
    created_date = models.DateField(verbose_name="Date created", auto_now_add=True)
    taken_date = models.DateField(verbose_name="Date taken", blank=True, null=True)

    def __str__(self):
        return f"Registered ID Card - Card Number: {self.card_number}, User: {self.citizen.first_name} {self.citizen.last_name}"





class RejectedIDCardApplication(models.Model):
    class RejectReason(models.TextChoices):
        SELECT = "", "Select Reason to reject"
        BAD_PICTURE = "Bad Picture", "Bad Picture"

    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    application = models.ForeignKey(IDCardRegistration, verbose_name="Application", related_name="rejected_application", on_delete=models.CASCADE)
    rejected_reason = models.CharField(verbose_name="Why rejected", choices=RejectReason.choices, default=RejectReason.BAD_PICTURE, max_length=20)
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return f"{self.rejected_reason},"




class LostIDCardReport(models.Model):
    class Status(models.TextChoices):
        SELECT = "", "Select Status"
        WAITING = "Waiting", "Waiting"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", related_name="lost_reports", on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, verbose_name="Lost Card ID number",)
    date_lost = models.DateField(verbose_name="When lost")
    description = models.TextField(verbose_name="Description")
    email = models.EmailField(verbose_name="Email Address", max_length=255, blank=False)
    contact_info = PhoneNumberField(verbose_name="Contact Info", blank=True, null=True)
    status = models.CharField(verbose_name="Status", choices=Status.choices, default=Status.WAITING, max_length=20)
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return f"Lost ID Card Report - Card Number: {self.card_number}, Citizen: {self.citizen}"



class Service(models.Model):
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    service_name = models.CharField(verbose_name="Service Title", max_length=100, blank=False, null=False, unique=True)
    requirements = models.TextField(verbose_name="Requirements", blank=False, null=False)

    def __str__(self):
        return self.service_name



class Publication(models.Model):
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(verbose_name="Title", max_length=255, blank=False, null=False)
    files = models.FileField(verbose_name="File", upload_to='publications/', blank=False, null=False)
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title