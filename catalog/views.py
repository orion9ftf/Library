from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import admin_required
from .models import Libro, Prestamo, Usuario
from .forms import LibroForm

def es_admin(user):
    return user.is_authenticated and user.rol == "admin"

class LibroListView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = "catalog/libros_list.html"
    context_object_name = "libros"

    def get_queryset(self):
        user = self.request.user

        # Admin ve todos los libros
        if user.rol == "admin":
            return Libro.objects.all()

        # Usuario normal → solo libros que ha solicitado por préstamo
        return Libro.objects.filter(prestamo__usuario=user).distinct()


class LibroDetailView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = "catalog/libro_detail.html"
    context_object_name = "libro"

    # No permitir que un usuario vea detalles de libros ajenos
    def dispatch(self, request, *args, **kwargs):
        libro = self.get_object()
        user = request.user

        if user.rol != "admin":
            # Verificar si el libro pertenece a ese usuario por préstamo
            tiene_prestamo = Prestamo.objects.filter(
                usuario=user, libro=libro
            ).exists()

            if not tiene_prestamo:
                return redirect("catalog:libros_list")

        return super().dispatch(request, *args, **kwargs)


@method_decorator(user_passes_test(es_admin), name="dispatch")
class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "catalog/libro_form.html"
    success_url = reverse_lazy("catalog:libros_list")


@method_decorator(user_passes_test(es_admin), name="dispatch")
class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = "catalog/libro_form.html"
    success_url = reverse_lazy("catalog:libros_list")


@method_decorator(user_passes_test(es_admin), name="dispatch")
class LibroDeleteView(DeleteView):
    model = Libro
    template_name = "catalog/libro_confirm_delete.html"
    success_url = reverse_lazy("catalog:libros_list")


class PrestamoListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = "catalog/prestamo_list.html"
    context_object_name = "prestamos"

    def get_queryset(self):
        user = self.request.user

        if user.rol == "admin":
            return Prestamo.objects.all()

        # Usuario normal - solo sus préstamos
        return Prestamo.objects.filter(usuario=user)


@login_required
def create_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)

    # Verificar disponibilidad
    if not libro.disponible and getattr(libro, "ejemplares", 1) == 0:
        messages.error(request, "El libro no está disponible para préstamo.")
        return redirect("catalog:libro_detail", pk=libro_id)

    # Crear préstamo usando el método del modelo
    prestamo = Prestamo(usuario=request.user, libro=libro)
    try:
        prestamo.registrar()
    except Exception as e:
        messages.error(request, f"No fue posible crear el préstamo: {e}")
        return redirect("catalog:libro_detail", pk=libro_id)

    messages.success(request, f"Préstamo creado: {libro.titulo}")
    return redirect("catalog:prestamo_list")


@login_required
def finalizar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)

    if request.user != prestamo.usuario and request.user.rol != "admin":
        messages.error(request, "No tienes permisos para finalizar este préstamo.")
        return redirect("catalog:prestamo_list")

    prestamo.finalizar()
    messages.success(request, "Préstamo finalizado correctamente.")
    return redirect("catalog:prestamo_list")

@method_decorator(user_passes_test(es_admin), name="dispatch")
class UsuarioListView(ListView):
    model = Usuario
    template_name = "catalog/usuario_list.html"
    context_object_name = "usuarios"
    paginate_by = 50


@method_decorator(user_passes_test(es_admin), name="dispatch")
class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = "catalog/usuario_detail.html"
    context_object_name = "usuario"


@user_passes_test(es_admin)
def cambiar_rol_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        nuevo_rol = request.POST.get("rol")
        if nuevo_rol in ("admin", "lector"):
            usuario.rol = nuevo_rol
            usuario.is_staff = (nuevo_rol == "admin")
            usuario.save()

            messages.success(request, f"Rol actualizado a '{nuevo_rol}'")
            return redirect("catalog:usuario_detail", pk=pk)

        messages.error(request, "Rol inválido.")

    return render(request, "catalog/usuario_cambiar_rol.html", {"usuario": usuario})
