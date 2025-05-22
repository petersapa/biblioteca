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
        self.esborrar_dades()
        self.crear_categories()
        self.crear_autors(10)
        self.crear_llibres(20)
        self.crear_alumnes(10)
        self.crear_prestecs(5)
        self.stdout.write('Dades creades correctament!')


    def esborrar_dades(self):
        self.stdout.write('Esborrant dades antigues...')
        Prestec.objects.all().delete()
        Llibre.objects.all().delete()
        Alumne.objects.all().delete()
        Autor.objects.all().delete()
        Categoria.objects.all().delete()

        # També esborrem usuaris generats (només els d'alumnes)
        User.objects.filter(username__startswith='alumne').delete()

    def crear_categories(self):
        self.stdout.write('Creant categories...')
        noms = ['Novel·la', 'Poesia', 'Humor', 'Història', 'Ficció', 'Misteri', 'Policíaca']
        for nom in noms:
            Categoria.objects.get_or_create(nom=nom)

    def crear_autors(self, n):
        self.stdout.write('Creant autors...')
        for _ in range(n):
            nom = fake.first_name()
            cognom = fake.last_name()
            Autor.objects.get_or_create(nom=nom, cognom=cognom)

    def crear_llibres(self, n):
        self.stdout.write('Creant llibres...')
        categories = list(Categoria.objects.all())
        autors = list(Autor.objects.all())
        for _ in range(n):
            Llibre.objects.create(
                titol=fake.catch_phrase(),
                descripcio = fake.paragraph(nb_sentences=8),
                isbn=fake.isbn13(),
                autor=random.choice(autors),
                categoria=random.choice(categories),
                prestat=False
            )

    def crear_alumnes(self, n):
        self.stdout.write('Creant alumnes...')
        cursos = ['DAW 1A', 'DAW 2A', 'ASIX 1A', 'ASIX 2A']
        for i in range(n):
            nom = fake.first_name()
            cognom = fake.last_name()
            username = f"{nom.lower()}.{cognom.lower()}"
            password = '1234'
            usuari = User.objects.create_user(username=username, password=password)
            usuari.first_name = nom
            usuari.last_name = cognom
            usuari.save()
            idalu = ''.join(fake.random_choices(elements='0123456789', length=random.randint(8, 12)))
            Alumne.objects.create(
                usuari=usuari,
                idalu=idalu,
                curs=random.choice(cursos)
            )

    def crear_prestecs(self, n):
        self.stdout.write('Creant prestecs...')
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