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
