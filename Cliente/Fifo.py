from ._anvil_designer import FifoTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Rowtemplatefifo import Rowtemplatefifo

class Fifo(FifoTemplate):
    def __init__(self, simulador, **properties):
        self.init_components(**properties)
        self.simulador = simulador  # Almacena el simulador seleccionado
        
        # Inicializa la lista de procesos
        self.procesos = []

    def agregar_click(self, **event_args):
        # Diccionario para almacenar el nuevo proceso
        nuevo_proceso = {}
        # Abre el formulario de ingreso de proceso
        save_clicked = alert(
            content=Rowtemplatefifo(item=nuevo_proceso),
            title="Agregar proceso",
            large=True,
            buttons=[("Guardar", True), ("Cancelar", False)],
        )
        # Verificaciones antes de guardar
        if save_clicked:
            # Obtiene los valores ingresados por el usuario
            codigo = nuevo_proceso.get('codigo')  # Asegúrate de obtener el código
            nombre = nuevo_proceso.get('nombre')
            tiempo = nuevo_proceso.get('tiempo')       
            beneficio = nuevo_proceso.get('beneficio')  # Asegúrate de obtener el beneficio       

            # Validaciones
            if not nombre or not codigo:  # Verifica que el nombre y código no estén vacíos
                alert("Error: El nombre y código del proceso no pueden estar vacíos.", title="Error", large=False)
                return

            if not str(tiempo).isdigit() or int(tiempo) <= 0:
                alert("Error: El tiempo debe ser un número positivo.", title="Error", large=False)
                return        

            # Agrega el proceso a la lista y actualiza el RepeatingPanel
            self.procesos.append((codigo, nombre, int(tiempo), float(beneficio)))        
            self.repeating_panel_1.items = [{'codigo': p[0], 'nombre': p[1], 'tiempo': p[2], 'beneficio': p[3]} for p in self.procesos]

    def ejecutarsimulacion_click(self, **event_args):
        # Verificar que haya procesos en el Repeating Panel
        if not self.repeating_panel_1.items or len(self.repeating_panel_1.items) == 0:
            alert("Error: No se han ingresado procesos. Debes agregar al menos un proceso.", title="Error")
            return

        # Validar que el costo por unidad sea un número válido
        costo_por_unidad_str = self.costo_unidad.text.strip()  # Obtener el texto de la caja de texto
        if not costo_por_unidad_str.isdigit() or float(costo_por_unidad_str) <= 0:
            alert("Error: El costo por unidad debe ser un número positivo.", title="Error", large=False)
            return

        costo_por_unidad = float(costo_por_unidad_str)  # Convertir a float
        procesos = []
        beneficio_total = 0  # Inicializa el beneficio total
        tiempo_total_ejecucion = 0  # Inicializa el tiempo total de ejecución

        for fila in self.repeating_panel_1.items:
            nombre = fila['nombre']
            tiempo = int(fila['tiempo'])
            beneficio = float(fila.get('beneficio', 0))  # Asegúrate de que tengas este campo disponible
            procesos.append((nombre, tiempo))  # Estructura como lista de tuplas
            
            # Acumula el beneficio total
            beneficio_total += beneficio

        # Llama al servidor para ejecutar la simulación FIFO
        logs, tiempo_total_ejecucion, total_procesos = anvil.server.call('ejecutar_simulacion_fifo', procesos)

        # Calcular costo total
        costo_total = tiempo_total_ejecucion * costo_por_unidad

        # Calcular margen total
        margen_total = beneficio_total - costo_total

        # Muestra los resultados en un TextArea (simulacion_resultado)
        self.simulacion_resultado.text += "\n".join(logs)
        self.simulacion_resultado.text += f"\nAlgoritmo seleccionado: {self.simulador}"
        self.simulacion_resultado.text += f"\nTiempo total de ejecución: {tiempo_total_ejecucion} segundos"
        self.simulacion_resultado.text += f"\nCantidad de procesos: {total_procesos}"
    
        # Agregar información financiera
        self.simulacion_resultado.text += f"\nBeneficio total: ${beneficio_total:.2f}"
        self.simulacion_resultado.text += f"\nCosto total: ${costo_total:.2f}"
        self.simulacion_resultado.text += f"\nMargen total: ${margen_total:.2f}"

        # Hacer visible botón más detalles
        self.masdetalles.visible = True

    def link_1_click(self, **event_args):
       open_form('Inicio')

    def masdetalles_click(self, **event_args):
      # Crear el diccionario `detalles` para `FormularioDetalles`
      tiempo_total_str = self.simulacion_resultado.text.split("\n")[-5]  # Obtener la línea del tiempo total
      tiempo_total = float(tiempo_total_str.split(":")[-1].strip().replace(" segundos", "").replace("$", "").replace(",", "").strip())
      print(f"el tiempo total es: {tiempo_total}")

      costo_por_unidad_str = self.costo_unidad.text.strip()  # Obtener costo por unidad del formulario
      costo_por_unidad = float(costo_por_unidad_str) if costo_por_unidad_str.isdigit() else 0

      detalles = {
          "procesos": [{"nombre": p[1], "tiempo_total": p[2], "beneficio": p[3]} for p in self.procesos],
          "tiempo_total": tiempo_total,
          "algoritmo": self.simulador,
          "costo_total": tiempo_total * costo_por_unidad,  # Calcular costo total aquí
      }
      print(detalles)  # Agrega esta línea para depuración
      open_form('FormularioDetallesfifo', detalles)
