from ._anvil_designer import FormularioDetallesfifoTemplate
from anvil import *
import plotly.graph_objects as go

class FormularioDetallesfifo(FormularioDetallesfifoTemplate):
    def __init__(self, detalles, **properties):
        self.init_components(**properties)

        # Verifica si `detalles` es un diccionario y contiene las claves necesarias
        if isinstance(detalles, dict):
            self.label_algoritmo.text = f"Algoritmo utilizado: {detalles.get('algoritmo', 'No especificado')}"
        else:
            alert("Error: los detalles no son un diccionario válido.")
            return

        # Preparar datos para el DataGrid
        tiempos_fifo = []
        for proceso in detalles.get('procesos', []):
            tiempos_fifo.append({
                'nombre': proceso.get("nombre", "Desconocido"),
                'tiempo_total': proceso.get("tiempo_total", "No disponible"),
                'beneficio': proceso.get("beneficio", 0),  # Asegúrate de incluir el beneficio
            })

        # Asignar datos de FIFO al DataGrid
        self.repeating_panel_1.items = tiempos_fifo

        # Configurar datos del gráfico de tiempo de ejecución total para FIFO
        nombres_procesos = [proceso.get("nombre", "Desconocido") for proceso in detalles.get('procesos', [])]
        tiempos_acumulados = [float(proceso.get("tiempo_total", 0)) for proceso in detalles.get('procesos', [])]

        fig_tiempo = go.Figure(data=go.Bar(
            x=nombres_procesos,
            y=tiempos_acumulados,
            name="Tiempo de ejecución por proceso",
            marker=dict(color='blue')
        ))

        fig_tiempo.update_layout(
            title='Tiempo de Ejecución por Proceso',
            xaxis_title='Nombre del Proceso',
            yaxis_title='Tiempo Total de Ejecución (segundos)'
        )

        self.plot_tiempo_procesos.figure = fig_tiempo

        # Calcular costos, beneficios y márgenes
        costo_total = detalles.get("costo_total", 0)
        beneficio_total = sum(proceso.get("beneficio", 0) for proceso in detalles.get('procesos', []))
        margen_total = beneficio_total - costo_total

        # Crear gráfico financiero
        fig_finanzas = go.Figure(data=[
            go.Bar(name="Beneficio Total", x=["Total"], y=[beneficio_total], marker=dict(color="green")),
            go.Bar(name="Costo Total", x=["Total"], y=[costo_total], marker=dict(color="red")),
            go.Bar(name="Margen Neto Total", x=["Total"], y=[margen_total], marker=dict(color="orange")),
        ])

        fig_finanzas.update_layout(
            title="Análisis Financiero",
            xaxis_title="Categoría",
            yaxis_title="Monto ($)",
            barmode="group",
        )

        self.plot_finanzas.figure = fig_finanzas

    def link_1_click(self, **event_args):
        open_form('Inicio')
