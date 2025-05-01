import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def ejecutar_simulacion_prioridad(procesos):
    logs = []
    tiempo_total_ejecucion = 0

    # Ordena los procesos por prioridad (segundo índice en la tupla)
    procesos_ordenados = sorted(procesos, key=lambda x: x[2])

    # Ejecuta cada proceso y acumula el tiempo total de ejecución
    for proceso in procesos_ordenados:
        nombre = proceso[0]
        tiempo = proceso[1]
        prioridad = proceso[2]
        
        # Suma el tiempo de cada proceso al tiempo total
        tiempo_total_ejecucion += tiempo
        logs.append(f"{nombre} (Prioridad: {prioridad}) ejecuta durante {tiempo} segundos.")
    
    # Cantidad total de procesos
    total_procesos = len(procesos)
    
    return logs, tiempo_total_ejecucion, total_procesos

