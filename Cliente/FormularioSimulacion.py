from ._anvil_designer import FormularioSimulacionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Rowtemplate import Rowtemplate

class Proceso:
    def __init__(self, id_proceso, tamanio):
        self.id_proceso = id_proceso
        self.tamanio = tamanio
        self.paginas = []  # Almacena las páginas asignadas

class Planificador:
    def __init__(self):
        self.procesos = []
        self.tamanio_memoria = 1024  # Valor por defecto, se puede cambiar desde el formulario
        self.tamanio_pagina = 256  # Tamaño de cada página
        self.paginas_libres = [i for i in range(self.tamanio_memoria // self.tamanio_pagina)]  # Páginas libres

    def agregar_proceso(self, proceso):
        num_paginas = (proceso.tamanio + self.tamanio_pagina - 1) // self.tamanio_pagina  # Redondeo hacia arriba
        if len(self.paginas_libres) >= num_paginas:
            for _ in range(num_paginas):
                pagina_asignada = self.paginas_libres.pop(0)
                proceso.paginas.append(pagina_asignada)
            self.procesos.append(proceso)  # Agregar el proceso a la lista
            return f"Proceso {proceso.id_proceso} ha sido asignado a las páginas: {proceso.paginas}"
        else:
            return "No hay suficiente memoria para ejecutar todos los procesos."

class FormularioSimulacion(FormularioSimulacionTemplate):
    def __init__(self, simulador, **properties):
        self.init_components(**properties)
        self.simulador = simulador
        self.procesos = []
        self.planificador = Planificador()  # Inicializa el planificador

    def agregar_click(self, **event_args):      
        nuevo_proceso = {}
    
        save_clicked = alert(
            content=Rowtemplate(item=nuevo_proceso),  
            title="Agregar proceso",
            large=True,
            buttons=[("Guardar", True), ("Cancelar", False)],
        )

        if save_clicked:
            try:
                codigo = nuevo_proceso.get('codigo', '').strip()
                nombre = nuevo_proceso.get('nombre', '').strip()
                tiempo = nuevo_proceso.get('tiempo')
                beneficio = nuevo_proceso.get('beneficio')

                # Validaciones ...
                
                tiempo = int(tiempo)
                beneficio = float(beneficio)

                # Crear un nuevo proceso y asignar memoria
                proceso_nuevo = Proceso(codigo, tiempo)
                resultado_asignacion = self.planificador.agregar_proceso(proceso_nuevo)

                # Agregar el proceso a la lista y actualizar el Repeating Panel
                self.procesos.append((codigo, nombre, tiempo, beneficio))
                self.repeating_panel_1.items = [
                    {'codigo': p[0], 'nombre': p[1], 'tiempo': p[2], 'beneficio': p[3]}
                    for p in self.procesos
                ]

                # Mostrar resultado de la asignación de memoria en el área de texto
                print(f"Asignación: {resultado_asignacion}")  # Print para seguimiento
                self.simulacion_resultado.text += f"\n{resultado_asignacion}"

            except Exception as e:
                alert(f"Ha ocurrido un error: {str(e)}", title="Error")

    def ejecutarsimulacion_click(self, **event_args):
      """
      Llama al servidor para ejecutar la simulación con los datos actuales.
      """
      if not self.procesos:
        alert("No hay procesos ingresados para simular.", title="Error")
        return

      try:
        # Leer la memoria disponible ingresada por el usuario
        memoria_disponible_texto = self.memoria_disponible.text.strip()  # Nombre correcto de la caja de texto
        
        if not memoria_disponible_texto.isdigit() or int(memoria_disponible_texto) <= 0:
            alert("Por favor ingresa una cantidad válida de memoria.", title="Error")
            return
        
        nueva_memoria_disponible = int(memoria_disponible_texto)

        print(f"Nueva memoria disponible: {nueva_memoria_disponible}")  # Para seguimiento

        if nueva_memoria_disponible != self.planificador.tamanio_memoria:
            print("Cambiando la memoria disponible...")  # Para seguimiento en terminal
            # Reiniciar el estado del planificador si cambia la memoria disponible
            self.planificador.procesos.clear()
            self.planificador.paginas_libres = [i for i in range(nueva_memoria_disponible // self.planificador.tamanio_pagina)]
        
        self.planificador.tamanio_memoria = nueva_memoria_disponible

        quantum = int(self.quantum.text)  # Quantum de la simulación
        costo_por_unidad = float(self.costo_unidad.text.strip())  # Costo por unidad de tiempo

        total_memoria_necesaria = sum(p[2] for p in self.procesos)  # Suponiendo que p[2] es el tamaño del proceso
        
        print(f"Total memoria necesaria: {total_memoria_necesaria}")  # Para seguimiento en terminal

        if total_memoria_necesaria > self.planificador.tamanio_memoria:
          mensaje_error = "No hay suficiente memoria para ejecutar todos los procesos."
          print(mensaje_error)  # Para seguimiento en terminal
            
          # Limpiar el área de texto antes de mostrar nuevos resultados.
          self.simulacion_resultado.text = f"\n{mensaje_error}"  # Aquí se limpia y muestra solo este mensaje
            
          return       
            
        procesos_para_simulacion = [(p[1], p[2]) for p in self.procesos]

        logs, tiempos_restantes_por_ronda = anvil.server.call(
            'ejecutar_simulacion', procesos_para_simulacion, quantum
        )

        tiempo_total_ejecucion = sum(p[2] for p in self.procesos)
        beneficio_total = sum(p[3] for p in self.procesos)
        costo_total = tiempo_total_ejecucion * costo_por_unidad 
        margen_neto = beneficio_total - costo_total 

        resultados_texto = "\n".join([
            f"El simulador seleccionado es: {self.simulador}",
            f"Tiempo total de ejecución: {tiempo_total_ejecucion} segundos",
            f"Número de procesos: {len(self.procesos)}",
            f"Costo Total de Ejecución: ${costo_total:.2f}",
            f"Beneficio Total: ${beneficio_total:.2f}",
            f"Margen Neto Total: ${margen_neto:.2f}",
        ])
        
        print(resultados_texto)  # Para seguimiento en terminal
        
        # Limpiar el área de texto antes de mostrar nuevos resultados.
        self.simulacion_resultado.text = ""  # Aquí se limpia el área de texto antes de agregar nuevos resultados.
        
        self.simulacion_resultado.text += resultados_texto
        
        # Guardar tiempos restantes para detalles y mostrar detalles solo si se ejecutaron correctamente.
        self.tiempos_restantes_por_ronda = tiempos_restantes_por_ronda
            
        if tiempos_restantes_por_ronda is not None:
          self.masdetalles.visible = True

      except ValueError as e:
          alert(f"Error: {str(e)}", title="Entrada inválida")


    def masdetalles_click(self, **event_args):
      """
      Muestra los detalles de la simulación.
      Este método no se llamará si no se ejecutaron procesos.
      """
      detalles = {
          "procesos": [{"nombre": p[1], "tiempo_total": p[2], "beneficio": p[3]} for p in self.procesos],
          "tiempo_total": sum(p[2] for p in self.procesos),
          "algoritmo": self.simulador,
          "tiempos_restantes": self.tiempos_restantes_por_ronda,
          "costo_por_unidad": float(self.costo_unidad.text.strip()),
      }
        
      open_form('FormularioDetalles', detalles)

    def link_1_click(self, **event_args):
      open_form('Inicio')
