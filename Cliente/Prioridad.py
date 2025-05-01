from ._anvil_designer import PrioridadTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Rowtemplateprioridad import Rowtemplateprioridad

class Prioridad(PrioridadTemplate):
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
        content=Rowtemplateprioridad(item=nuevo_proceso),
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
        prioridad = nuevo_proceso.get('prioridad')

        # Validaciones
        if not nombre or not codigo:  # Verifica que el nombre y código no estén vacíos
            alert("Error: El nombre y código del proceso no pueden estar vacíos.", title="Error", large=False)
            return

        if not str(tiempo).isdigit() or int(tiempo) <= 0:
            alert("Error: El tiempo debe ser un número positivo.", title="Error", large=False)
            return

        if prioridad is None:  # Verifica que se haya seleccionado una prioridad
            alert("Error: Por favor, selecciona una prioridad válida.", title="Error", large=False)
            return

        # Agrega el proceso a la lista y actualiza el RepeatingPanel
        self.procesos.append((codigo, nombre, int(tiempo), int(prioridad), beneficio))        
        self.repeating_panel_1.items = [{'codigo': p[0], 'nombre': p[1], 'tiempo': p[2], 'prioridad': p[3], 'beneficio': p[4]} for p in self.procesos]

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
      costo_total = 0      # Inicializa el costo total

      for fila in self.repeating_panel_1.items:        
        nombre = fila['nombre']
        tiempo = int(fila['tiempo'])
        prioridad = int(fila['prioridad'])
        beneficio = float(fila['beneficio'])  # Asegúrate de que sea un número

        procesos.append((nombre, tiempo, prioridad))  # Estructura como lista de tuplas
        beneficio_total += beneficio  # Acumula el beneficio
        costo_total += tiempo * costo_por_unidad  # Calcula el costo usando el costo por unidad ingresado

      # Llama al servidor para ejecutar la simulación de prioridad
      logs, tiempo_total_ejecucion, total_procesos = anvil.server.call('ejecutar_simulacion_prioridad', procesos)

      # Muestra los resultados en un TextArea (simulacion_resultado)
      self.simulacion_resultado.text += "\n".join(logs)
      self.simulacion_resultado.text += f"\nNombre del algoritmo: {self.simulador}"
      self.simulacion_resultado.text += f"\nTiempo total de ejecución: {tiempo_total_ejecucion} segundos"
      self.simulacion_resultado.text += f"\nCantidad de procesos: {total_procesos}"
    
      # Agrega la información general
      self.simulacion_resultado.text += f"\nBeneficio total: ${beneficio_total:.2f}"
      self.simulacion_resultado.text += f"\nCosto total: ${costo_total:.2f}"
    
      # Calcula y muestra el margen total
      margen_total = beneficio_total - costo_total
      self.simulacion_resultado.text += f"\nMargen total: ${margen_total:.2f}"


    def link_1_click(self, **event_args):
       open_form('Inicio')


    def masdetalles_click(self, **event_args):
      # Crear el diccionario `detalles` para `FormularioDetalles`
      detalles = {
        "procesos": [{"codigo": p[0], "nombre": p[1], "tiempo_total": p[2], "beneficio": p[4], "prioridad": p[3]} for p in self.procesos],
        "tiempo_total": self.simulacion_resultado.text.split("\n")[-2],
        "algoritmo": self.simulador,
        "costo_por_unidad": float(self.costo_unidad.text.strip()),  # Obtener costo por unidad del formulario
      }
      print(detalles)  # Agrega esta línea
      open_form('FormularioDetallesprioridad', detalles)


