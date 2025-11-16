from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "catalog"
urlpatterns = [
    # LIBROS
    path('libros/', views.LibroListView.as_view(), name='libros_list'),
    path('libros/<int:pk>/', views.LibroDetailView.as_view(), name='libro_detail'),
    path('libros/crear/', views.LibroCreateView.as_view(), name='libro_create'),
    path('libros/<int:pk>/editar/', views.LibroUpdateView.as_view(), name='libro_edit'),
    path('libros/<int:pk>/eliminar/', views.LibroDeleteView.as_view(), name='libro_delete'),

    # PRESTAMOS
    path('prestamos/', views.PrestamoListView.as_view(), name='prestamo_list'),
    path('prestamos/crear/<int:libro_id>/', views.create_prestamo, name='prestamo_create'),
    path('prestamos/<int:pk>/finalizar/', views.finalizar_prestamo, name='prestamo_finalizar'),

    # USUARIOS (ADMIN)
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_detail'),
    path('usuarios/<int:pk>/cambiar-rol/', views.cambiar_rol_usuario, name='usuario_cambiar_rol'),

    # LOGIN / LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # HOME
    path('', views.LibroListView.as_view(), name='inicio'),
]
