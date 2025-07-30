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

## Principios SOLID