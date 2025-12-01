from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# usuario custom para poder añadir 'rol'
class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('lector', 'Lector'),
        ('editor', 'Editor'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='lector')

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.email})"
    
class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True)
    disponible = models.BooleanField(default=True)
    # campo opcional - ver a futuro
    ejemplares = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def cambio_estado(self, prestado=True):
        if prestado:
            # si hay ejemplares, decrementar y marcar no disponible si llega a 0 - ver luego
            if self.ejemplares > 0:
                self.ejemplares -= 1
            if self.ejemplares == 0:
                self.disponible = False
        else:
            self.ejemplares += 1
            self.disponible = True
        self.save()

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='prestamos')
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE, related_name='prestamos')
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def registrar(self):
        """Lógica para registrar préstamo: marcar libro como prestado y guardar"""
        # ejemplo: marcar libro prestado
        # si se gestiona ejemplares, cambiar a -> cambio_estado()
        if not self.libro.disponible and self.libro.ejemplares == 0:
            raise ValueError("Libro no disponible")
        # disminuir ejemplares / cambiar estado
        self.libro.cambio_estado(prestado=True)
        self.save()

    def finalizar(self):
        """Finaliza préstamo y devuelve libro"""
        if self.finalizado:
            return
        self.finalizado = True
        self.fecha_fin = timezone.now()
        self.libro.cambio_estado(prestado=False)
        self.save()

    def __str__(self):
        return f"Préstamo {self.id}: {self.libro} a {self.usuario}"
