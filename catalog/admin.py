from django.contrib import admin
from .models import Usuario, Libro, Prestamo
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    fieldsets = (*UserAdmin.fieldsets, )
    list_display = ('username', 'email', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff')


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'disponible', 'ejemplares')
    search_fields = ('titulo', 'autor')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'libro', 'usuario', 'fecha_inicio', 'fecha_fin', 'finalizado')
    list_filter = ('finalizado',)
    search_fields = ('libro__titulo', 'usuario__username')

# validar los usuarios ya creados en local sqlite
