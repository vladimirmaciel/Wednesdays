from django.db import models
from django.contrib.auth.models import User # fazemos esta importação para uar o user do django


class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address',blank=True)
    email_address = models.EmailField('Email',blank=True)

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    frist_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.frist_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE) #  informa ao Django para ativar o efeito de exclusão, isto é, continuar excluindo os modelos dependentes também
    #  venue = models.CharField(max_length=120)
    # manager = models.CharField(max_length=60)
    manager = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL) # relacionado com User do django
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name
