import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import time
import plotly.graph_objects as go

@anvil.server.callable
def verificar_proceso(codigo):
    """
    Verifica si el código del proceso existe en la tabla de procesos
    y devuelve el nombre y el beneficio.
    """
    proceso = app_tables.procesos.get(pro_cod=codigo)  # Busca por el código único
    if proceso:
        return {'pro_nom': proceso['pro_nom'], 'pro_ben': proceso['pro_ben']}
    else:
        return None


@anvil.server.callable
def ejecutar_simulacion(procesos, quantum, algoritmo="Round Robin"):
    """
    Ejecuta la simulación del algoritmo Round Robin.
    """
    tiempo_total_ejecucion = 0
    logs = []
    tiempos_restantes_por_ronda = []

    while any(tiempo > 0 for _, tiempo in procesos):
        ronda_tiempos = []

        for i, (nombre, tiempo) in enumerate(procesos):
            if tiempo > 0:
                tiempo_ejec = min(quantum, tiempo)
                tiempo -= tiempo_ejec
                tiempo_total_ejecucion += tiempo_ejec
                procesos[i] = (nombre, tiempo)

                logs.append(f"{nombre} ejecutándose por {tiempo_ejec} segundos")
                logs.append(f"{nombre} tiene {tiempo} segundos restantes")
                ronda_tiempos.append((nombre, tiempo))

        tiempos_restantes_por_ronda.append(ronda_tiempos)

    logs.append(f"El simulador seleccionado es: {algoritmo}")
    logs.append(f"El tiempo total de ejecución es: {tiempo_total_ejecucion} segundos")
    logs.append(f"La cantidad de procesos es: {len(procesos)}")

    return logs, tiempos_restantes_por_ronda

@anvil.server.callable
def generar_grafico_rondas(tiempos_por_proceso):
    """
    Genera un gráfico JSON para las rondas de ejecución de los procesos.
    """ 
    # Crear las trazas para cada proceso
    trazas = []
    for nombre, tiempos in tiempos_por_proceso.items():
        trazas.append(go.Bar(
            x=list(range(1, len(tiempos) + 1)),  # Números de ronda
            y=tiempos,  # Tiempos ejecutados
            name=f"Proceso {nombre}"  # Etiqueta de cada proceso
        ))
    
    # Crear la figura con todas las trazas
    fig_rondas = go.Figure(data=trazas)
    fig_rondas.update_layout(
        title='Tiempos de Ejecución por Ronda (Round Robin)',
        xaxis_title='Número de Ronda',
        yaxis_title='Tiempo Ejecutado (segundos)',
        barmode='stack'
    )

    # Convertir la figura a JSON y devolverla
    return fig_rondas.to_json()