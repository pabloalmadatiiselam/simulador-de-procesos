# 🧠 Simulador de Planificación de Procesos

Este proyecto es un **simulador educativo** desarrollado con [Anvil](https://anvil.works), que permite visualizar y probar distintos algoritmos de planificación de procesos utilizados por los sistemas operativos.

## 🎯 Objetivo

Simular y comparar el comportamiento de algoritmos como:
- FIFO (First In, First Out)
- Round Robin
- Prioridades (estáticas)
- Otros algoritmos propuestos por el docente

Este simulador fue desarrollado como parte de una práctica de la asignatura **Sistemas Operativos** en una institución de nivel secundario.

## 📁 Estructura del Proyecto

```
simulador-de-procesos/
├── cliente/           # Código de la interfaz visual (formularios de Anvil)
├── servidor/          # Código Python del servidor (funciones y lógica)
├── base_de_datos/     # Archivo CSV exportado desde la tabla interna de Anvil
└── README.md          # Información general del proyecto
```

## 💡 Características

- Interfaz intuitiva desarrollada en Anvil
- Lógica del simulador implementada con Python
- Uso de una tabla interna de Anvil para almacenar los procesos
- Simulación paso a paso o automática para observar los resultados

## 📊 Base de Datos

La tabla interna de procesos fue exportada como archivo CSV (`procesos.csv`) y se encuentra en la carpeta `base_de_datos/`. Puede abrirse fácilmente con un editor de texto o una planilla de cálculo.

## 📌 Requisitos

- Navegador web moderno para ejecutar el simulador en Anvil (si se desea probar)
- Cuenta gratuita en [Anvil](https://anvil.works) si se quiere importar y modificar

## 👨‍💻 Autor

**Pablo Daniel Almada**  
📧 Correo: pabloj94g@gmail.com  
🌐 Portfolio: [https://pabloalmadatiiselam.github.io/pf/](https://pabloalmadatiiselam.github.io/pf/)
