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

<!--### Diagrama de Casos de Uso UML-->

<!--![Diagrama de Casos de Uso](docs/diagramaUML.png)-->

### Prototipo (GUI)

La interfaz principal incluye:
- Página de inicio con información general.
- Barra de navegación para acceso a funcionalidades.
- Secciones para anuncios, notas, reportes y gestión de usuarios.

![Prototipo GUI](https://www.figma.com/design/mePETDXZAzFnH5TMuKuZg2/Dise%C3%B1o-Software?node-id=0-1&p=f&t=159E8ZY7anSn5hm4-0)

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

## Vista General de Arquitectura

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