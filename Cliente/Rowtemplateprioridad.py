from ._anvil_designer import RowtemplateprioridadTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Rowtemplateprioridad(RowtemplateprioridadTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.prioridad.items = [
    ("", None),        # Opción en blanco
    ("Alta", 1),       # Visible: "Alta", Interno: 1
    ("Media", 2),      # Visible: "Media", Interno: 2
    ("Baja", 3)        # Visible: "Baja", Interno: 3
    ]

    self.prioridad.selected_value = None  # Establecer el valor seleccionado inicial como None

    # Any code you write here will run before the form opens.

  def codigo_lost_focus(self, **event_args):
    """
    Busca el nombre y beneficio del proceso al perder el foco en el campo código.
    """
    try:
      codigo = self.codigo.text.strip()  # Obtiene el código ingresado
      if not codigo:
        alert("Por favor, ingresa un código de proceso.", title="Error")
        return

      # Llama al servidor para verificar el proceso
      proceso = anvil.server.call('verificar_proceso', codigo)
      print(f"Datos recuperados del servidor: {proceso}")

      if proceso:
        # Actualiza los valores en las cajas de texto y el diccionario `item`
        self.nombre.text = proceso['pro_nom']
        self.beneficio.text = str(proceso['pro_ben'])
        self.item['nombre'] = proceso['pro_nom']
        self.item['beneficio'] = proceso['pro_ben']
        print(f"Nombre: {self.nombre.text}, Beneficio: {self.beneficio.text}")
      else:
        alert(f"No se encontró el proceso con código {codigo}.", title="Proceso no encontrado")
        self.nombre.text = ""
        self.beneficio.text = ""
        self.item['nombre'] = ""
        self.item['beneficio'] = ""

    except Exception as e:
      alert(f"Ha ocurrido un error: {str(e)}", title="Error")

