from django.db import models

class user (models.Model):
    nume = models.CharField(max_length=30)
    prenume = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    parola = models.CharField(max_length=32)
    tip_persoana = models.CharField(max_length=10)   # fizica/juridica
    companie = models.CharField(max_length=60)
    adresa = models.CharField(max_length=150)
    status_cos = models.BooleanField()      # True = cos plin gata pt reciclare
                                            # False, nu e plin, nu e gata de preluare

    def __str__(self):
        return self.nume + self.prenume

