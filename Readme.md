## Biblioteca


```sh
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser # solo para crear usuarios (usar con responsabilidad)
$ python manage.py runserver # levantar el servidor
```

```sh
Diagrama de Clases
Clase Usuario

Atributos:
id: identificador único del usuario.
nombre: nombre del usuario.
email: correo electrónico.
password: contraseña.
rol: tipo de usuario (por ejemplo, administrador o lector).

Métodos:
registrar(): permite crear un nuevo usuario en el sistema.
autenticar(): valida las credenciales para iniciar sesión.

Clase Libro
Atributos:

id: identificador único del libro.
titulo: nombre del libro.
autor: autor del libro.
disponible: indica si el libro está disponible o prestado.

Método:
cambioEstado(): cambia el estado de disponibilidad del libro ("por ejemplo, al ser prestado o devuelto").

Clase Préstamo
Atributos:

id: identificador único del préstamo.
usuario_id: referencia al usuario que realiza el préstamo.
libro_id: referencia al libro prestado.
fecha_inicio: fecha en que comienza el préstamo.
fecha_fin: fecha en que finaliza el préstamo.

Métodos:
registrar(): crea un nuevo préstamo.
finalizar(): marca el préstamo como finalizado y actualiza el estado del libro.
```

### Relaciones / Modelos:
```sh
Un Usuario puede tener uno o varios Préstamos.
Un Libro puede estar asociado a cero o un Préstamo activo.
La clase Préstamo actúa como intermediaria entre Usuario y Libro.
```

### Diagrama de clases (modelo Django)

![diagrama_clases](/catalog/static/img/diagrama_clases.png)


### Diagrama de secuencia

![diagrama](/catalog/static/img/diagrama_de_secuencia.png)


### Diagrama de actividades
![diagrama_de_actividades](/catalog/static/img/diagrama_de_actividades.png)

### DIAGRAMA DE COMUNICACIÓN / INTERACCIÓN

El diagrama de comunicación muestra la relación estructural entre los objetos
que intervienen en el caso de uso “Solicitar préstamo”.

#### Objetos involucrados:
```sh
Usuario → solicita el préstamo.
Vista (Interfaz) → recibe la solicitud.
Controlador → gestiona la lógica de negocio.
Modelo Libro → verifica disponibilidad.
Modelo Préstamo → registra el préstamo y actualiza datos.
```

#### Secuencia estructurada:

1. Usuario envía solicitud a la Vista.
2. Vista comunica al Controlador el requerimiento.
3. Controlador consulta a Modelo Libro por disponibilidad.
4. Modelo Libro responde con el estado del libro.
5. Si disponible, Controlador crea instancia en Modelo Préstamo.
6. Modelo Préstamo actualiza el estado del libro y responde a Controlador.
7. Controlador notifica a la Vista el resultado final.

***Este diagrama refleja la colaboración entre objetos y flujo de mensajes,
complementando el diagrama de secuencia.***

## Levantamiento de Requerimientos:

1. Planificación del levantamiento
2. Stakeholders indentificados:
    * Administrador del sistema: controla catálogos y usuarios.
    * Usuario final (lector): iimplementan el sistema.
    * Desarrolladores: implementan el sistema.
    * Docente o cliente académico: valida requerimientos y calidad.

Cronograma resumido:

1. Identificación de actores y alcance.
2. Entrevista con administrador para requerimientos funcionales.
3. Prototipo rápido de interfaz.
4. Validación de requerimientos y ajustes.

## Implementación de estándares de calidad

Aplicacioes de Normas:

* ISO/IEC 25010: Se garantiza la calidad mediante mantenibilidad, funcionalidad y seguridad.
* ISO/IEC 12207: Se aplica en las fases de análisis, diseño, implementación y validación.
* ISO/IEC 14764: Considerada para mantenimiento y futuras versiones del sistema.


### Cambiar el rol:

```shell
$ python manage.py shell
# y ahora:
$ from catalog.models import Usuario

# Buscar el usuario por nombre
user = Usuario.objects.get(username="nombre_del_usuario") # acá le pasas el usuario y puedes cambiar su rol

# Cambiar el rol
user.rol = "admin"

# (opcional) darle permisos de staff y superuser
user.is_staff = True
user.is_superuser = True
user.save()
print("Rol actualizado correctamente:", user.rol)
```

### Poblar la db:

La librería Faker tiene la particularidad de poblar la base de datos con usuarios de prueba, o nombre de libros, o contraseñas (no recomendado una vez en la nube).

```shell
$ pip install Faker
$ python manage.py shell
from faker import Faker
from catalog.models import Usuario
fake = Faker()

# ejemplo: crear 10 usuarios falsos con rol lector
for _ in range(10):
    Usuario.objects.create(
        nombre=fake.name(),
        correo=fake.email(),
        rol='lector',
        password='123456'
    )

print("Usuarios creados con éxito.")
```

## Se trabaja bajo la Metodología Ágil

Se utiliza Jira para la asignación de tarjetas con historias de usuarios, las cuales fueron implementadas de manera gradual por Sprint.
![jira](/catalog/static/img/area_de_trabajo.png)


### Modo visual del sitio
#### Catálogo de Libros
![sitio](/catalog/static/img/catalogo_libros.png)

### Préstamos de Libros
![prestamos](/catalog/static/img/prestamo_libros.png)

### Usuarios / vista de una Administradora/or 
![usuario](/catalog/static/img/usuarios.png)

### Cambiar el rol

De Lector a Admin
![cambio_rol](/catalog/static/img/cambo_de_rol.png)



```pgsql
id SERIAL PK
nombre VARCHAR NOT NULL
email VARCHAR UNIQUE NOT NULL
password_hash VARCHAR NOT NULL
rol VARCHAR NOT NULL (lector|admin)
fecha_creacion TIMESTAMP DEFAULT now()

id SERIAL PK
titulo VARCHAR NOT NULL
autor VARCHAR
isbn VARCHAR UNIQUE
categoria VARCHAR
copias_total INTEGER DEFAULT 1
copias_disponibles INTEGER DEFAULT 1
portada_url VARCHAR
descripcion TEXT


id SERIAL PK
usuario_id INTEGER FK usuario(id)
libro_id INTEGER FK libro(id)
fecha_inicio TIMESTAMP NOT NULL
fecha_fin_prevista TIMESTAMP NOT NULL
fecha_devolucion TIMESTAMP NULLABLE
estado VARCHAR (activo|devuelto|vencido)

```

```sql

CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  rol VARCHAR(20) NOT NULL,
  fecha_creacion TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE libro (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(255) NOT NULL,
  autor VARCHAR(255),
  isbn VARCHAR(20) UNIQUE,
  categoria VARCHAR(100),
  copias_total INTEGER NOT NULL DEFAULT 1,
  copias_disponibles INTEGER NOT NULL DEFAULT 1,
  portada_url TEXT,
  descripcion TEXT
);

CREATE TABLE prestamo (
  id SERIAL PRIMARY KEY,
  usuario_id INTEGER NOT NULL REFERENCES usuario(id),
  libro_id INTEGER NOT NULL REFERENCES libro(id),
  fecha_inicio TIMESTAMP NOT NULL,
  fecha_fin_prevista TIMESTAMP NOT NULL,
  fecha_devolucion TIMESTAMP,
  estado VARCHAR(20) NOT NULL DEFAULT 'activo',
  CONSTRAINT un_libro_un_prestamo CHECK (estado IN ('activo','devuelto','vencido'))
);

```

*****************************************************************
## FrontEnd

