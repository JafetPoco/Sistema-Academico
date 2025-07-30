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
  - [Convenciones de codificacion PEP8 para python](#convenciones-de-codificacion-pep8-para-python)
  - [Codificacion limpia (Clean Code)](#codificacion-limpia-clean-code)
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

## Convenciones de codificacion PEP8 para python

## Codificacion limpia (Clean Code)
Aplicamos un conjunto de principios y prácticas de Clean Code para desarrollar este proyecto. Nuestro objetivo es que el código sea fácil de leer, entender, mantener y extender a lo largo del tiempo.

### Variables
Utilizamos nombres claros y descriptivos para variables, funciones, clases y archivos, de modo que reflejen su propósito real dentro del sistema.
#### Ejemplo:
En **app/infrastructure/repository/repository.py**, se define con nombres claros y descriptivos para las varibles:
```python
class CourseRepository(BaseRepository):
    dto = CourseDTO
    mapper = CourseMapper

    def get_courses_by_professor(self, professor_id):
        ...
```
**CourseRepository** indica claramente que se trata de un repositorio para manejar cursos.
**get_courses_by_professor** describe con precisión qué hace el método: obtener los cursos dictados por un profesor.
**professor_id** como parámetro deja claro que se espera un identificador de profesor, no de otra entidad.

### Funciones
Cada clase o función se enfoca en hacer una sola cosa. Esto facilita las pruebas, el mantenimiento y la comprensión del sistema.
#### Ejemplo:
En **app/application/services/auth_service.py**, la clase AuthService tiene responsabilidades claras y bien separadas:
```python
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

### Clases
Modelamos las clases para encapsular datos y comportamientos relacionados, asegurándome de que cada clase tuviera una única responsabilidad siempre que fue posible.
#### Ejemplo de clase con responsabilidad definida:
En **app/infrastructure/repository/repository.py**
```python
class CourseRepository:
     # Responsabilidad: Gestionar el acceso y manipulación de datos de cursos
     def get_courses_by_professor(self, professor_id):
         ...
     def get_all_courses(self):
         ...
```

#### I. Single Responsibility Principle (SRP)
Principio de Responsabilidad Única
##### Ejemplo:
En **app/domain/services/course_service.py**
```python
class CourseService:
    # Única responsabilidad: Lógica de negocio relacionada con los cursos
     def get_courses_by_professor(self, professor_id: int):
        # Lógica para obtener cursos por profesor y aplicar validaciones de dominio.
        ...
```
En **app/application/announcement_controller.py**
```python
class AnnouncementController:
     # Única responsabilidad: Manejar las solicitudes HTTP relacionadas con los anuncios.
     def get_all_announcements(self):
         # Delega la lógica de negocio a AnnouncementService.
         ...
```
#### II. Open/Closed Principle (OCP)
Principio Abierto/Cerrado, abiertas para extensión, pero cerradas para modificación.
##### Ejemplo:
En app/infrastructure/repository/repository.py
```python
class BaseRepository:
    # Métodos CRUD genéricos
    def add(self, entity):
        ...
    def get_by_id(self, entity_id):
        ...

class UserRepository(BaseRepository):
    # Se extiende BaseRepository sin modificarla
    def get_user_by_email(self, email):
        # Lógica específica para usuarios
        ...

class CourseRepository(BaseRepository):
    # Se extiende BaseRepository sin modificarla
    def get_courses_by_professor(self, professor_id):
        # Lógica específica para cursos
        ...
```
#### III. Liskov Substitution Principle (LSP)
Principio de Sustitución de Liskov

##### Ejemplo:
En app/infrastructure/repository/repository.py
```python
class BaseRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def add(self, entity):
        # Lógica común para añadir una entidad
        self.db_session.add(entity)
        self.db_session.commit()
        return entity

    def get_by_id(self, model, entity_id):
        # Lógica común para obtener por ID
        return self.db_session.query(model).get(entity_id)

class UserRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = User # Asumiendo que User es el modelo para UserRepository

    # Puede añadir métodos específicos o sobrescribir si es necesario,
    # pero debe mantener la coherencia con BaseRepository
    def get_user_by_email(self, email: str):
        return self.db_session.query(self.model).filter_by(email=email).first()

class CourseRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = Course # Asumiendo que Course es el modelo para CourseRepository

    # Puede añadir métodos específicos o sobrescribir
    def get_courses_by_professor(self, professor_id: int):
        # Lógica específica para cursos por profesor
        return self.db_session.query(self.model).filter_by(professor_id=professor_id).all()
```
La existencia de una clase base BaseRepository de la que heredan repositorios 

#### IV. Interface Segregation Principle (ISP)
Principio de Segregación de Interfaces
##### Ejemplo:
En app/infrastructure/repository/repository.py, Los repositorios se comportan como interfaces segregadas para sus respectivos clientes.
```python
class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session
        # ... métodos específicos de usuario ...
    def get_user_by_email(self, email: str):
        # ...
        pass
    def save_user(self, user):
        # ...
        pass

class CourseRepository:
    def __init__(self, db_session):
        self.db_session = db_session
        # ... métodos específicos de curso ...
    def get_all_courses(self):
        # ...
        pass
    def get_courses_by_professor(self, professor_id: int):
        # ...
        pass
```
En app/domain/services/auth_service.py, (un "cliente" del UserRepository).
```python
class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    def register_user(self, username, email, password, role_id):
        # AuthService solo interactúa con UserRepository, no con CourseRepository
        user = self.user_repository.save_user(User(username=username, email=email, password=password, role_id=role_id))
        return user
```
En app/domain/services/course_service.py (un "cliente" del CourseRepository)
```python
class CourseService:
    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository
    def get_courses_for_professor(self, professor_id: int):
        # CourseService solo interactúa con CourseRepository, no con UserRepository
        return self.course_repository.get_courses_by_professor(professor_id)
```

#### V. Dependency Inversion Principle (DIP)
Principio de Inversión de Dependencias
##### Ejemplo:
En app/application/admin_controller.py se observa claramente,AdminService es una abstracción para el controlador 
```python
from app.domain.services.admin_service import AdminService

class AdminController:
    def __init__(self, admin_service: AdminService):
        self.admin_service = admin_service
```
 
En app/domain/services/admin_service.py tambien exite una abstraccion, UserRepository es una abstracción para el servicio
```python
from app.infrastructure.repository.repository import UserRepository

class AdminService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        ...
```

### Don't Repeat Yourself (DRY)
Evitamos repetir lógica innecesaria en distintas partes del sistema.

#### Ejemplo:
En **app/infrastructure/repository/repository.py**, se definió una clase base llamada BaseRepository que centraliza las operaciones comunes como agregar, eliminar, actualizar y obtener registros desde la base de datos:
```python
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
```python
def enroll_user(self, user_id: int, course_id: int):
    """Matricular un usuario en un curso"""
    try:
        # Verificar si ya existe
        if self.is_user_enrolled(user_id, course_id):
            return None, "El usuario ya está matriculado en este curso"
```

## Principios SOLID