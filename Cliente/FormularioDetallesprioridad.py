from ._anvil_designer import FormularioDetallesprioridadTemplate
from anvil import *
import plotly.graph_objects as go

class FormularioDetallesprioridad(FormularioDetallesprioridadTemplate):
    def __init__(self, detalles, **properties):
        self.init_components(**properties)

        # Verifica si `detalles` es un diccionario y contiene las claves necesarias
        if isinstance(detalles, dict):
            #self.label_tiempo_total.text = f"{detalles.get('tiempo_total', 'No disponible')} segundos"
            self.label_algoritmo.text = f"Algoritmo utilizado: {detalles.get('algoritmo', 'No especificado')}"
        else:
            alert("Error: los detalles no son un diccionario válido.")
            return

        # Añadir el nuevo label como título para el DataGrid
        #self.label_titulo_grid = Label(text="Lista de Procesos Ordenados por Prioridad", 
                                       #font_size=20,  # Ajusta el tamaño de la fuente según sea necesario
                                       #align="center")  # Centrar el texto
        #self.add_component(self.label_titulo_grid)  # Agrega el label al formulario

        # Ordenar los procesos por prioridad (de menor a mayor)
        procesos_ordenados = sorted(detalles.get("procesos", []), key=lambda x: x.get("prioridad", float("inf")))

        # Preparar datos ordenados para el DataGrid
        tiempos_prioridad = [
            {
                "codigo": proceso.get("codigo", "Desconocido"),
                "nombre": proceso.get("nombre", "Desconocido"),
                "tiempo_total": proceso.get("tiempo_total", "No disponible"),
                "beneficio": proceso.get("beneficio", "No disponible"),
                "prioridad": proceso.get("prioridad", "No disponible"),
            }
            for proceso in procesos_ordenados
        ]

        # Asignar datos ordenados al DataGrid
        self.repeating_panel_1.items = tiempos_prioridad

        # Configurar datos para el gráfico de tiempos
        nombres_procesos = [proceso.get("nombre", "Desconocido") for proceso in procesos_ordenados]
        tiempos_acumulados = [proceso.get("tiempo_total", 0) for proceso in procesos_ordenados]

        # Crear gráfico de barras para el tiempo de ejecución
        fig_tiempo = go.Figure(
            data=go.Bar(
                x=nombres_procesos,
                y=tiempos_acumulados,
                name="Tiempo de ejecución por proceso",
                marker=dict(color="blue"),
            )
        )

        fig_tiempo.update_layout(
            title="Tiempo de Ejecución por Proceso (Ordenado por Prioridad)",
            xaxis_title="Nombre del Proceso",
            yaxis_title="Tiempo Total de Ejecución (segundos)",
        )

        self.plot_tiempo_procesos.figure = fig_tiempo

        # Calcular costos, beneficios y márgenes
        costo_por_unidad = detalles.get("costo_por_unidad", 0)
        
        # Extraer beneficios y tiempos para el análisis financiero
        beneficios = [float(proceso.get("beneficio", 0)) for proceso in procesos_ordenados]
        tiempos = [float(proceso.get("tiempo_total", 0)) for proceso in procesos_ordenados]
        
        # Calcular costos basados en los tiempos y costo por unidad
        costos = [t * costo_por_unidad for t in tiempos]
        
        # Calcular márgenes netos
        margenes_netos = [b - c for b, c in zip(beneficios, costos)]

        # Crear gráfico de barras para los análisis financieros
        fig_finanzas = go.Figure(data=[
            go.Bar(name="Beneficio Total", x=["Total"], y=[sum(beneficios)], marker=dict(color="green")),
            go.Bar(name="Costo Total", x=["Total"], y=[sum(costos)], marker=dict(color="red")),
            go.Bar(name="Margen Neto Total", x=["Total"], y=[sum(margenes_netos)], marker=dict(color="orange")),
        ])
        
        fig_finanzas.update_layout(
            title="Análisis Financiero Total",
            xaxis_title="Categoría",
            yaxis_title="Monto ($)",
            barmode="group",
        )

        self.plot_finanzas.figure = fig_finanzas

    def link_1_click(self, **event_args):
      open_form('Inicio')
      pass
