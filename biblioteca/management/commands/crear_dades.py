from django.core.management.base import BaseCommand
from biblioteca.models import Autor, Categoria, Llibre, Alumne, Prestec
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone

fake = Faker(["es_CA","es_ES"])

class Command(BaseCommand):
    help = "Crea dades de prova per a la biblioteca"

    def handle(self, *args, **kwargs):
        self.crear_categories()
        self.crear_autors(10)
        self.crear_llibres(20)
        self.crear_alumnes(10)
        self.crear_prestecs(5)
        self.stdout.write(self.style.SUCCESS('✅ Dades de prova creades amb èxit!'))

    def crear_categories(self):
        noms = ['Novel·la', 'Poesia', 'Ciència', 'Història', 'Ficció']
        for nom in noms:
            Categoria.objects.get_or_create(nom=nom)

    def crear_autors(self, n):
        for _ in range(n):
            nom = fake.first_name()
            cognom = fake.last_name()
            Autor.objects.get_or_create(nom=nom, cognom=cognom)

    def crear_llibres(self, n):
        categories = list(Categoria.objects.all())
        autors = list(Autor.objects.all())
        for _ in range(n):
            Llibre.objects.create(
                titol=fake.sentence(nb_words=4),
                isbn=fake.isbn13(),
                autor=random.choice(autors),
                categoria=random.choice(categories),
                prestat=False
            )

    def crear_alumnes(self, n):
        cursos = ['1r ESO', '2n ESO', '3r ESO', '4t ESO']
        for i in range(n):
            username = f'alumne{i}'
            usuari, _ = User.objects.get_or_create(username=username)
            usuari.set_password('1234')
            usuari.save()
            Alumne.objects.get_or_create(
                usuari=usuari,
                idalu=f"A{i:03}",
                curs=random.choice(cursos)
            )

    def crear_prestecs(self, n):
        alumnes = list(Alumne.objects.all())
        llibres_disponibles = list(Llibre.objects.filter(prestat=False))

        for _ in range(min(n, len(llibres_disponibles))):
            alumne = random.choice(alumnes)
            llibre = llibres_disponibles.pop()
            data_prestec = timezone.now() - timedelta(days=random.randint(1, 14))
            Prestec.objects.create(
                alumne=alumne,
                llibre=llibre,
                data_prestec=data_prestec
            )
            # Marca el llibre com a prestat
            llibre.prestat = True
            llibre.save()