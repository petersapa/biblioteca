from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nom = models.CharField(max_length=100)
    cognom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.cognom}"

class Categoria(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Llibre(models.Model):
    titol = models.CharField(max_length=200)
    descripcio = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    prestat = models.BooleanField(default=False)

    def __str__(self):
        return self.titol

class Alumne(models.Model):
    usuari = models.OneToOneField(User, on_delete=models.CASCADE)
    idalu = models.CharField(max_length=20, unique=True)
    curs = models.CharField(max_length=50)

    def __str__(self):
        return self.usuari.get_full_name()

class Prestec(models.Model):
    alumne = models.ForeignKey(Alumne, on_delete=models.CASCADE)
    llibre = models.ForeignKey(Llibre, on_delete=models.CASCADE)
    data_prestec = models.DateField(auto_now_add=True)
    data_devolucio = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.llibre.titol} a {self.alumne.usuari.username}"