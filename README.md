# Sistema-Academico EDUNET

## Índice

- [Sistema-Academico EDUNET](#sistema-academico-edunet)
  - [Índice](#índice)
  - [Integrantes](#integrantes)
  - [Propósito](#propósito)
    - [Funcionalidades de Alto Nivel](#funcionalidades-de-alto-nivel)
    - [Diagrama de Casos de Uso UML](#diagrama-de-casos-de-uso-uml)
    - [Prototipo (GUI)](#prototipo-gui)
  - [Modelo de Dominio Clean Architecture](#modelo-de-dominio-clean-architecture)
    - [Estructura de Carpetas](#estructura-de-carpetas)
    - [Principales Entidades](#principales-entidades)
    - [Módulos](#módulos)
  - [Requisitos](#requisitos)
- [Practicas de desarrollo de software](#practicas-de-desarrollo-de-software)
  - [Reporte SonarLint](#reporte-sonarlint)
    - [1. Literales de Cadena Duplicadas](#1-literales-de-cadena-duplicadas)
    - [2. Clase/Funcion/Metodo no cumple la convención de nombres (python:S101)](#2-clasefuncionmetodo-no-cumple-la-convención-de-nombres-pythons101)
    - [3. MySQL database passwords should not be disclosed (secrets:S6697)](#3-mysql-database-passwords-should-not-be-disclosed-secretss6697)
    - [4. Unused local variables should be removed (python:S1481)](#4-unused-local-variables-should-be-removed-pythons1481)
  - [Convenciones de codificacion PEP8 para python](#convenciones-de-codificacion-pep8-para-python)
  - [Codificacion limpia (Clean Code)](#codificacion-limpia-clean-code)
    - [Nombres significativos](#nombres-significativos)
      - [Ejemplo:](#ejemplo)
    - [Funciones con responsabilidad unica](#funciones-con-responsabilidad-unica)
      - [Ejemplo:](#ejemplo-1)
    - [Evitar código duplicado](#evitar-código-duplicado)
      - [Ejemplo:](#ejemplo-2)
    - [Comentarios útiles y mínimos](#comentarios-útiles-y-mínimos)
    - [Ejemplo:](#ejemplo-3)
  - [Principios SOLID](#principios-solid)


## Integrantes
- ALEXANDER HUAYHUA PEREZ
- JAFET POCO CHIRE
- BERLY DUEÑAS MANDAMIENTOS
- FERNANDO A. SUCA QUISPE
- RONALD VENTURA VENERO


## Propósito

**EDUNET** es un sistema académico digital diseñado para conectar a estudiantes, padres y docentes en una sola plataforma. Permite la gestión de notas, anuncios y comunicación eficiente dentro de la comunidad educativa, facilitando el acceso seguro y centralizado a la información escolar.

---

### Funcionalidades de Alto Nivel

- Consulta de notas y calificaciones por estudiantes y padres.
- Publicación de anuncios por parte de administradores.
- Gestión de usuarios (padres, profesores, administradores).
- Visualización de actividades académicas y reportes.

### Diagrama de Casos de Uso UML

![Diagrama de Casos de Uso](docs/DiagramaCasosDeUso.png)

### Prototipo (GUI)

La interfaz principal incluye:
- Página de inicio con información general.
- Barra de navegación para acceso a funcionalidades.
- Secciones para anuncios, notas, reportes y gestión de usuarios.

[Prototipo GUI](https://www.figma.com/design/mePETDXZAzFnH5TMuKuZg2/Dise%C3%B1o-Software?node-id=0-1&p=f&t=159E8ZY7anSn5hm4-0)

![Prototipo](docs/gui_prototipo.png)

---

## Modelo de Dominio Clean Architecture

### Estructura de Carpetas
```
Sistema-Academico/
├── app/
│   ├── routes/
│   ├── application/
│   ├── domain/
│   │   └── services/
│   └── infrastructure/
│       └── repository/
├── docs/
├── static/
└── templates/
```

### Principales Entidades

- **Usuario**: Base para Estudiante, Profesor, Padre, Administrador.
- **Curso**: Relaciona estudiantes y profesores.
- **Anuncio**: Publicado por profesores/administradores.
- **Calificación**: Asociada a estudiantes y cursos.
- **Asistencia**: Registro de asistencia por curso y estudiante.

### Módulos

- `domain/entities`: Entidades y repositorios del dominio.
- `infrastructure/repository`: Implementaciones de acceso a datos.
- `domain/services`: Lógica de negocio y servicios de aplicación.
- `application`: Controladores.
- `routes`: Endpoints web.
- `templates`: Plantillas HTML para la GUI.
- `config`: Configuración de la aplicación.

---

![Diagrama de Clases Arquitectura](docs/diagramaUML.png)

- **app/domain/services**: Servicios de aplicación (notificaciones, reportes).
- **app/domain/entities**: Entidades y contratos del dominio.
- **infrastructure/repository**: Implementaciones de acceso a datos.
- **app/application**: Controladores Flask.
- **templates**: Vistas HTML (Jinja2).

---

## Requisitos

- Python 3.12+
- Flask
- SQLAlchemy
- MySQL Connector
- dotenv
- Base de datos relacional MySQL

Instalar dependencias:
```bash
pip install -r requirements.txt
```

# Practicas de desarrollo de software

## Reporte SonarLint

### 1. Literales de Cadena Duplicadas  
**Regla:** `python:S1192`  
**Descripción:** String literals should not be duplicated  
**Ubicación:** Múltiples archivos (por ejemplo, `repository.py`, `controller.py`)  
**Tipo:** Code Smell

Se encontraron múltiples ocurrencias de literales como `'courses.course_id'` y `'users.user_id'`.  
Esto puede dificultar el mantenimiento y la refactorización del código.

**Solución:**

Definir constantes con nombres descriptivos:
```
COURSE_ID = 'courses.course_id'
USER_ID = 'users.user_id'
```

### 2. Clase/Funcion/Metodo no cumple la convención de nombres (python:S101)

**Regla:** `python:S101`  
**Descripción:** Los nombres de las clases deben coincidir con una expresión regular configurada (por defecto: `^_?([A-Z_][a-zA-Z0-9]*|[a-z_][a-z0-9_]*)$`).  
**Ubicación:** Clase `Anuncio_rep`  
**Tipo:** Code Smell

El nombre `Anuncio_rep` no coincide con la convención recomendada (CapWords o snake_case para clases utilizadas como callables).  

**Solución:**

Renombrar la clase respetando “PascalCase”, por ejemplo:

```python
class AnnouncementRepository:
    ...
```

De la misma forma usando snake_case para las funciones:

```python
def get_announcement_by_id(self, announcement_id):
    ...
```

### 3. MySQL database passwords should not be disclosed (secrets:S6697)

**Regla:** `secrets:S6697`  
**Descripción:** Si una contraseña de base de datos MySQL aparece en el código fuente, puede ser divulgada accidentalmente y comprometer la seguridad del sistema.  
**Ubicación:** Literales visibles de contraseñas en archivos de código o configuración.  
**Tipo:** Vulnerabilidad (Security Hotspot)

La presencia de contraseñas en texto plano facilita su exposición, ya sea por inspección del código, logs o análisis.

**Solución recomendada:**

- Mover la contraseña a un archivo de configuración externo que no forme parte del control de versiones  usando el paquete dotenv y un archivo `.env`:
- Asegurarse de que esa ubicación tenga permisos restringidos.
- Cargar la contraseña en tiempo de ejecución desde variables de entorno o archivos seguros, evitando integrarla en el código.

```ini
# .env
MYSQL_PASSWORD=mi_password_segura
```

### 4. Unused local variables should be removed (python:S1481)

**Regla:** `python:S1481`  
**Descripción:** Las variables locales declaradas pero no utilizadas deben eliminarse. Mantener variables no usadas degrada la legibilidad y puede indicar código innecesario o errores potenciales ([Sonar](https://rules.sonarsource.com/python/RSPEC-1481)) :contentReference[oaicite:0]{index=0}

Ejemplo no conforme:

```python
def handle_create(self, form_data: dict, user_id: int):
    title = form_data.get('title', '').strip()
    content = form_data.get('content', '').strip()
    is_private = bool(form_data.get('is_private'))
    course_id = form_data.get('course_id') or None  # Optional

    if not title or not content:
        return "danger", "Título y contenido son obligatorios."

    created, err = self.service.create()

    if err:
        return "danger", f"Error al crear el anuncio: {err}"

    return "success", "Anuncio creado correctamente."
```

En este ejemplo, la variable `created` se define pero no se utiliza en el resto de la función, lo que genera una advertencia de SonarLint.

**Solución:**
Utilizar `_` para indicar que la variable no se usará, o eliminarla si no es necesaria:


## Convenciones de codificacion PEP8 para python

## Codificacion limpia (Clean Code)
Aplicamos un conjunto de principios y prácticas de Clean Code para desarrollar este proyecto. Nuestro objetivo es que el código sea fácil de leer, entender, mantener y extender a lo largo del tiempo.

### Nombres significativos
Utilizamos nombres claros y descriptivos para variables, funciones, clases y archivos, de modo que reflejen su propósito real dentro del sistema.
#### Ejemplo:
En **app/infrastructure/repository/repository.py**, se define con nombres claros y descriptivos para las varibles:
```bash
class CourseRepository(BaseRepository):
    dto = CourseDTO
    mapper = CourseMapper

    def get_courses_by_professor(self, professor_id):
        ...
```
**CourseRepository** indica claramente que se trata de un repositorio para manejar cursos.
**get_courses_by_professor** describe con precisión qué hace el método: obtener los cursos dictados por un profesor.
**professor_id** como parámetro deja claro que se espera un identificador de profesor, no de otra entidad.
### Funciones con responsabilidad unica
Cada clase o función se enfoca en hacer una sola cosa. Esto facilita las pruebas, el mantenimiento y la comprensión del sistema.
#### Ejemplo:
En **app/application/services/auth_service.py**, la clase AuthService tiene responsabilidades claras y bien separadas:
```bash
class AuthService:
    def register_user(self, user_data): ...
    def authenticate(self, email, password): ...
    def validate_registration_data(self, user_data): ...
    def get_role_display_name(self, role): ...
    def can_access_qualification(self, user, student_id): ...
    def is_admin(self, user): ...
    def get_user_permissions(self, user): ...

```
**register_user**: Encargada del proceso de registro de usuarios.
**authenticate**: Verifica las credenciales de acceso.
**validate_registration_data**: Realiza validaciones sobre los datos de entrada antes del registro.
**get_role_display_name, can_access_qualification, is_admin, get_user_permissions**: Gestionan aspectos específicos del rol del usuario.
### Evitar código duplicado
Evitamos repetir lógica innecesaria en distintas partes del sistema. Cuando detectamos que varias clases o funciones hacen lo mismo, extraemos esa lógica en una función o clase reutilizable.
Esto sigue el principio **DRY (Don’t Repeat Yourself)**, que ayuda a mantener el código limpio, fácil de modificar y menos propenso a errores.

#### Ejemplo:
En **app/infrastructure/repository/repository.py**, se definió una clase base llamada BaseRepository que centraliza las operaciones comunes como agregar, eliminar, actualizar y obtener registros desde la base de datos:
```bash
class BaseRepository:
    def add(self, domain_obj): ...
    def remove(self, obj_id): ...
    def update(self, obj_id, data): ...
    def get(self, obj_id): ...
    def list_all(self): ...

```
Luego, los repositorios específicos como UserRepository, CourseRepository, GradeRepository, etc., heredan esta clase y **evitan duplicar** la misma lógica en cada uno.
### Comentarios útiles y mínimos
En el proyecto evitamos comentarios innecesarios que solo repiten lo que el código ya expresa. En su lugar, agregamos comentarios solo cuando es necesario explicar el por qué de una decisión, el propósito de una operación compleja o una validación importante.
### Ejemplo:
En **app/infrastructure/repository/repository.py**, los métodos del EnrollmentRepository usan comentarios breves y precisos antes de funciones específicas para dejar claro qué hacen sin redundar:
```bash
def enroll_user(self, user_id: int, course_id: int):
    """Matricular un usuario en un curso"""
    try:
        # Verificar si ya existe
        if self.is_user_enrolled(user_id, course_id):
            return None, "El usuario ya está matriculado en este curso"
```

## Principios SOLID