import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def ejecutar_simulacion_fifo(procesos):
    logs = []
    tiempo_total_ejecucion = 0

    # Ejecuta cada proceso en el orden en que se ingresaron
    for nombre, tiempo in procesos:
        tiempo_total_ejecucion += tiempo
        logs.append(f"{nombre} ejecuta durante {tiempo} segundos.")
    
    total_procesos = len(procesos)
    
    return logs, tiempo_total_ejecucion, total_procesos
