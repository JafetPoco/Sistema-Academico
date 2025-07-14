# Sistema-Academico

## Propósito

**EDUNET** es un sistema académico digital diseñado para conectar a estudiantes, padres y docentes en una sola plataforma. Permite la gestión de notas, anuncios, actividades académicas y comunicación eficiente dentro de la comunidad educativa, facilitando el acceso seguro y centralizado a la información escolar.

---

### Funcionalidades de Alto Nivel

- Consulta de notas y calificaciones por estudiantes y padres.
- Publicación de anuncios por parte de profesores y administradores.
- Gestión de usuarios (estudiantes, padres, profesores, administradores).
- Visualización de actividades académicas y reportes.
- Notificaciones automáticas para padres y estudiantes.

### Diagrama de Casos de Uso UML

![Diagrama de Casos de Uso](docs/DiagramaCasosDeUso.png)

### Prototipo (GUI)

La interfaz principal incluye:
- Página de inicio con información general.
- Barra de navegación para acceso a funcionalidades.
- Secciones para anuncios, notas, reportes y gestión de usuarios.

[Prototipo GUI](https://www.figma.com/design/mePETDXZAzFnH5TMuKuZg2/Dise%C3%B1o-Software?node-id=0-1&p=f&t=159E8ZY7anSn5hm4-0)

---

## Modelo de Dominio

#### Principales Entidades

- **Usuario**: Base para Estudiante, Profesor, Padre, Administrador.
- **Curso**: Relaciona estudiantes y profesores.
- **Anuncio**: Publicado por profesores/administradores.
- **Calificación**: Asociada a estudiantes y cursos.
- **Asistencia**: Registro de asistencia por curso y estudiante.

#### Módulos

- `domain/models`: Entidades y repositorios del dominio.
- `domain/repositories`: Implementaciones de acceso a datos.
- `app/services`: Lógica de negocio y servicios de aplicación.
- `interfaces/controllers`: Controladores y endpoints web.
- `interfaces/templates`: Plantillas HTML para la GUI.
- `config`: Configuración de la aplicación.

---

![Diagrama de Clases Arquitectura](docs/diagramaUML.png)

#### Estructura de Carpetas
```
Sistema-Academico/ 
│ ├── app/ 
│   └── services/ 
├── config/ 
├── domain/ 
│ ├── models/ 
│ └── repositories/ 
├── interfaces/ 
│ ├── controllers/ 
│ ├── static/ 
│ └── templates/ 
└── requirements.txt
```
- **app/services**: Servicios de aplicación (notificaciones, reportes).
- **domain/models**: Entidades y contratos del dominio.
- **domain/repositories**: Implementaciones de acceso a datos.
- **interfaces/controllers**: Controladores Flask.
- **interfaces/templates**: Vistas HTML (Jinja2).
- **config**: Configuración global.

---

## Requisitos

- Python 3.12+
- Flask
- SQLAlchemy
- MySQL Connector

Instalar dependencias:
```bash
pip install -r requirements.txt
```
## 📝 Convenciones de Codificación Aplicadas

### 1. 📁 Organización modular: paquete `reporte`

**Práctica:**  
Se creó un paquete llamado `reporte` para agrupar plantillas y componentes relacionados. Esto sigue la convención de paquetes en Python, donde un paquete es un directorio con un archivo `__init__.py`.

**Estructura:**
```

/reporte/
├── __init__.py
├── layout_reporte.html
└── reporte.html
````
---

### 2. 📄 Nombres de archivos HTML en `snake_case`

**Práctica:**  
Se usa `snake_case` en los archivos de plantilla HTML (`layout_reporte.html`, `reporte.html`) para mantener consistencia con las convenciones de nombres de archivos en Python y facilitar su uso en `render_template()`.

**Ejemplo:**
```python
return render_template('reporte/reporte.html')
````

---

### 3. ⚙️ Separación de configuración (archivo `config/default.py`)

**Práctica:**
Se agregaron las variables de configuración de la base de datos en un archivo independiente, lo cual sigue el principio de separación de responsabilidades y facilita el mantenimiento.

**Convención de codificación aplicada (PEP 8):**
Las constantes (como configuraciones globales) están nombradas usando mayúsculas con guiones bajos (UPPER_CASE_WITH_UNDERSCORES), que es la convención recomendada para constantes en Python.

**Fragmento:**

```python
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "*******"
MYSQL_DB = "edunet"
MYSQL_PORT = 3306
```
---

### 4. 🔗 Registro de rutas mediante `Blueprint` (en `run.py`)

**Práctica:**
Se utilizó el sistema de Blueprints de Flask para registrar rutas específicas del módulo `reporte`, lo cual mejora la escalabilidad y modularidad del proyecto.

**Fragmento en `run.py`:**

```python
from interfaces.controllers.reporte_controlador import reporte_bp
app.register_blueprint(reporte_bp)
```

---

### 5. 🐍 Convenciones de nombres en `reporte_controlador.py`

**Prácticas aplicadas:**

* `snake_case` para el nombre del archivo: `reporte_controlador.py`
* `snake_case` para funciones: `mostrar_reporte()`
* Uso de variables descriptivas: `reporte_bp`
* Organización modular mediante `Blueprint`

**Fragmento de código:**

```python
from flask import Blueprint, render_template

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reporte')

@reporte_bp.route('/')
def mostrar_reporte():
    return render_template('reporte/reporte.html')
```
