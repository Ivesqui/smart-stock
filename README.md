# smart-stock
Smart-Stock is an intelligent inventory management system that combines stock control, demand forecasting, and automated purchase recommendations using data-driven decision models.

## Sistema de Gestión de Inventarios

Este repositorio contiene el desarrollo de un API **Sistema de Gestión de Inventarios**, implementado como parte de las prácticas de la asignatura **Programación Orientada a Objetos**, utilizando el lenguaje **Python** y aplicando principios fundamentales de la **POO**, junto con persistencia de datos mediante **SQLite**.

El sistema permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre productos, simulando el funcionamiento básico de un inventario real para una tienda o negocio pequeño.

---

## 📌 Descripción del Proyecto

El Sistema de Gestión de Inventarios es una aplicación de consola que permite:

- Registrar productos en un inventario.
- Gestionar productos mediante un identificador de negocio (SKU).
- Actualizar cantidades y precios.
- Buscar productos por nombre o SKU.
- Listar todos los productos almacenados.
- Persistir la información de forma segura usando una base de datos SQLite.

El proyecto está diseñado siguiendo una **arquitectura modular**, separando claramente la lógica de negocio, los modelos, la interfaz de usuario y la persistencia de datos.

---

## 🎯 Objetivos del Proyecto

- Aplicar los fundamentos de la Programación Orientada a Objetos.
- Implementar clases, encapsulamiento y modularización.
- Desarrollar un CRUD funcional con persistencia de datos.
- Separar responsabilidades siguiendo buenas prácticas de diseño.
- Simular un sistema de inventario similar a los utilizados en entornos reales.

---

## ⚙️ Funcionalidades del Sistema

El sistema ofrece las siguientes funcionalidades:

1. **Añadir producto**
   - Registra un nuevo producto en el inventario.
   - El ID es generado automáticamente por la base de datos.
   - El SKU debe ser único.

2. **Eliminar producto**
   - Elimina un producto utilizando su SKU.

3. **Actualizar producto**
   - Permite modificar la cantidad y/o el precio de un producto existente.
   - La actualización se realiza mediante el SKU.

4. **Buscar producto**
   - Permite buscar productos por nombre o por SKU.
   - Soporta coincidencias parciales.

5. **Listar inventario**
   - Muestra todos los productos registrados en la base de datos.

6. **Salir del sistema**
   - Finaliza la ejecución del programa de forma segura.

---

## 🆔 Identificadores: ID y SKU

El sistema maneja dos tipos de identificadores:

### 🔹 ID (Identificador técnico)
- Es un campo **autoincrementable**.
- Es gestionado automáticamente por SQLite.
- No es visible ni manipulable por el usuario.
- Se utiliza internamente para la base de datos.

### 🔹 SKU (Stock Keeping Unit)
- Es un identificador de negocio.
- Es ingresado por el usuario.
- Debe ser único.
- Se utiliza para eliminar, actualizar y buscar productos.

### 📦 Formato del SKU

El SKU sigue el siguiente formato:

```
Ejemplos:
- `ALM-001` → Alimentos
- `LIM-002` → Limpieza
- `BEB-003` → Bebidas
- `FER-001` → Ferretería

Este formato facilita la identificación del tipo de producto y es comúnmente utilizado en sistemas reales de inventario.
```

## 🗂️ Estructura del Proyecto

```
smart-stock
├src/
│ ├── core/
│ │ ├── entities/
│ │ │  ├── product.py
│ │ │  └── user.py
│ │ └── interfaces/
│ ├── interfaces/
│ │ └── product_repository.py 
│ ├── infrastructure/
│ │ └── database/
│ │    └── conect.py
│ ├── security/
│ │ ├── decorators.py
│ │ ├── hash_utils.py
│ │ └── jwt_utils.py
│ ├── services/
│ │ ├── init.py
│ │ ├── auth_service.py
│ │ ├── inventory_service.py
│ │ └── report_excel_service.py 
│ ├── tests/
│ ├── web/
│ │ └── app.py 
│ ├── _init_.py
│ ├── inventory.db
│ └── main.py
└── README.md
```

# Actualizaciones

Arquitectura en capas

Separación de responsabilidades

Seguridad con hashing

JWT

Decorators

Inyección de dependencias manual