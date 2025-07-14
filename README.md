
# Estilos de Programación Aplicados

Este proyecto implementa diversos **estilos de programación**, los cuales permiten una estructura clara, mantenible y coherente en todas sus capas. A continuación se detallan con ejemplos concretos del código.



## 1. Cookbook

Este estilo se refleja en la estructura modular del código, donde cada función realiza una tarea bien definida y aislada.

Ejemplo en `curso_repositorio_impl.py`:

```python
def obtener(self, session, id):
    return session.query(curso).filter_by(curso_id=id).first()

def agregar(self, session, curso):
    session.add(curso)
    session.commit()
````

En el controlador, cada ruta se encarga de una acción específica:

```python
@curso_bp.route('/cursos', methods=['GET'])
def mostrar_cursos():
    session = get_session()
    cursos = repositorio.obtener_todos(session)
    return render_template('cursos/cursos.html', cursos=cursos)
```

---

## 2. Error/Exception Handling

Se utiliza manejo de excepciones para capturar errores durante operaciones críticas como la manipulación de la base de datos:

```python
try:
    repositorio.agregar(session, nuevo_curso)
    flash("Curso creado exitosamente.", "success")
except SQLAlchemyError:
    flash("Error al crear el curso. Intente más tarde.", "danger")
```

En la vista (`cursos.html`), se notifican al usuario los mensajes con `get_flashed_messages`:

```html
{% for category, message in messages %}
  <div class="alert alert-{{ category }}">{{ message }}</div>
{% endfor %}
```

---

## 3. Persistent-Tables

Mediante el uso de SQLAlchemy como ORM, los objetos se vinculan directamente a tablas de base de datos:

```python
class curso(Base):
    __tablename__ = 'cursos'

    curso_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    profesor_id = Column(Integer, ForeignKey('profesores.profesor_id'))
```

Las operaciones CRUD se realizan sobre estas entidades persistentes.

---

## 4. Things

El diseño está centrado en entidades del mundo real, como `curso`, que se representa en todas las capas:

* Modelo:

  ```python
  class curso(Base)
  ```
* Repositorio:

  ```python
  repositorio.obtener(session, curso_id)
  ```
* Vista:

  ```html
  {{ curso.nombre }}
  ```

Este enfoque basado en objetos concretos del dominio es típico del estilo *Things*.

---

## 5. RESTful (Parcial)

Aunque no es una API REST completa (no responde con JSON), la aplicación adopta convenciones REST en sus rutas y uso de métodos HTTP:

* `GET /cursos`: Listar cursos
* `POST /cursos`: Crear curso
* `POST /cursos/eliminar/<id>`: Eliminar curso
* `GET /cursos/<id>`: Ver detalle

Ejemplo en Flask:

```python
@curso_bp.route('/cursos/eliminar/<int:curso_id>', methods=['POST'])
def eliminar_curso(curso_id):
    session = get_session()
    repositorio.eliminar(session, curso_id)
    return redirect(url_for('curso.mostrar_cursos'))
```

Formulario HTML correspondiente:

```html
<form method="POST" action="{{ url_for('curso.eliminar_curso', curso_id=curso.curso_id) }}">
    <button type="submit">Eliminar</button>
</form>

