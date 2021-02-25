from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Korisnici(AbstractUser):
    rola = [
        ('mentor','mentor'),
        ('student','student'),
        ]
    stat = [
        ('none','none'),
        ('izvanredni','izvanredni'),
        ('redovni','redovni'),
        ]
    #korisnik_id = models.AutoField(max_length=64, primary_key=True)
    #email = models.CharField(max_length=64, null= False, unique=True)
    role = models.CharField(max_length=7, null=False, choices=rola)
    status = models.CharField(max_length=10, null=False, choices=stat)
    REQUIRED_FIELDS = ['email', 'role', 'status', 'password']
    def __str__(self):
        USERNAME_FIELD = 'email'
        return self.email



class Predmeti(models.Model):
    izb = [
        ('da','da'),
        ( 'ne', 'ne'),
        ]
    #predmet_id = models.AutoField(null=False, max_length=64, primary_key=True)
    ime = models.CharField(max_length=255, null= False)
    kod = models.CharField(max_length=16, null=False, unique=True)
    program = models.TextField(null=False)
    bodovi = models.PositiveIntegerField( null= False)
    sem_redovni = models.PositiveIntegerField(null= False)
    sem_izvanredni = models.IntegerField( null= False)
    izborni = models.CharField(max_length=2, null=False, choices=izb)
    def __str__(self):
        return self.ime

class Upisi(models.Model):
    Status = [
       ('enrolled','enrolled'),
        ('passed', 'passed'),
        ('not_passed','not_passed'),
    ]

    korisnici_id = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    predmeti_id = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, null=False, choices=Status)
    repeat_subj = models.IntegerField(null= False, default=0)
    def __str__(self):
        return str(self.id)