from django.core.management.base import BaseCommand
from faker import Faker
from catalog.models import Usuario

class Command(BaseCommand):
    help = 'Pobla la base de datos con usuarios de prueba'

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(10):
            Usuario.objects.create(
                nombre=fake.name(),
                correo=fake.email(),
                rol='lector',
                password='123456'
            )
        self.stdout.write(self.style.SUCCESS('Usuarios creados con éxito'))
# $ python manage.py poblar_datos
"""
  Libro.objects.create(
    titulo=fake.sentence(nb_words=3),
    autor=fake.name(),
    fecha_publicacion=fake.date(),
    categoria=fake.word()
)
"""
