from ._anvil_designer import FormularioDetallesTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class FormularioDetalles(FormularioDetallesTemplate):
    def __init__(self, detalles, **properties):
        self.init_components(**properties)

        if isinstance(detalles, dict):
            #self.label_tiempo_total.text = f"{detalles.get('tiempo_total', 'No disponible')}"
            self.label_algoritmo.text = f"Algoritmo utilizado: {detalles.get('algoritmo', 'No especificado')}"
        else:
            alert("Error: los detalles no son un diccionario válido.")
            return

        # Procesar el DataGrid con tiempos restantes por ronda
        tiempos_por_ronda = []
        for ronda, tiempos in enumerate(detalles['tiempos_restantes']):
            for proceso in tiempos:
                # Se asegura de que cada proceso tiene los elementos esperados.
                tiempos_por_ronda.append({
                    'ronda': ronda + 1,
                    'nombre': proceso[0] if len(proceso) > 0 else "Desconocido",
                    'tiempo_restante': proceso[1] if len(proceso) > 1 else "No disponible"
                })
        
        # Verifica que `tiempos_por_ronda` tenga datos y los asigna al DataGrid
        print("Contenido de tiempos_por_ronda:", tiempos_por_ronda)  # Para depuración
        self.repeating_panel_1.items = tiempos_por_ronda

        # Configurar datos para el gráfico de tiempo de ejecución acumulado
        nombres_procesos = [proceso.get("nombre", "Desconocido") for proceso in detalles['procesos']]
        tiempos_acumulados = [proceso.get("tiempo_total", 0) for proceso in detalles['procesos']]

        # Configuración y creación del gráfico de barras para tiempo de ejecución por proceso
        fig_tiempos = go.Figure(data=go.Bar(
            x=nombres_procesos,
            y=tiempos_acumulados,
            name="Tiempo de ejecución por proceso",
            marker=dict(color='blue')
        ))

        fig_tiempos.update_layout(
            title='Tiempo de Ejecución por Proceso',
            xaxis_title='Nombre del Proceso',
            yaxis_title='Tiempo Total de Ejecución (segundos)'
        )

        self.plot_tiempo_procesos.figure = fig_tiempos

        # Calcular y crear gráfico para información financiera
        costo_por_unidad = detalles.get("costo_por_unidad", 0)
        
        # Asegurarse de que hay procesos antes de calcular beneficios
        if detalles['procesos']:
            beneficio_total = sum(p.get('beneficio', 0) for p in detalles['procesos'])  # Sumar beneficios
            tiempo_total_ejecucion = sum(p.get('tiempo_total', 0) for p in detalles['procesos'])  # Sumar tiempos
            costo_total = tiempo_total_ejecucion * costo_por_unidad  # Costo total
            margen_neto = beneficio_total - costo_total  # Margen neto

            # Datos para el gráfico financiero
            fig_finanzas = go.Figure(data=[
                go.Bar(name='Beneficio Total', x=['Beneficio Total'], y=[beneficio_total]),
                go.Bar(name='Costo Total', x=['Costo Total'], y=[costo_total]),
                go.Bar(name='Margen Neto', x=['Margen Neto'], y=[margen_neto])
            ])

            fig_finanzas.update_layout(
                title='Análisis Financiero',
                barmode='group',
                xaxis_title='Categoría',
                yaxis_title='Monto ($)'
            )

            self.plot_finanzas.figure = fig_finanzas

    def link_1_click(self, **event_args):
      open_form('Inicio')
      
