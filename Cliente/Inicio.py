from ._anvil_designer import InicioTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Inicio(InicioTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Configura las opciones del dropdown
    self.simuladores.items = ["", "Round Robin", "Prioridad", "FIFO"]       

  def simuladores_change(self, **event_args):
    # Obtén la selección actual
        seleccion = self.simuladores.selected_value
        # Redirige al formulario correspondiente según la selección
        if seleccion == "Round Robin":
            open_form('FormularioSimulacion', simulador=seleccion)  # Abre el formulario de Round Robin
        elif seleccion == "Prioridad":
            open_form('Prioridad', simulador=seleccion)  # Abre el formulario de Prioridad
        elif seleccion == "FIFO":
            open_form('Fifo', simulador=seleccion)  # Abre el formulario FIFO

  #def link_6_click(self, **event_args): 
    ## URL del PDF almacenado en Google Drive
    #pdf_url = "https://drive.google.com/file/d/1uxMEnJ9On4-bYUBXRhzojsdq4EQSev2M/view?usp=sharing"  # Reemplaza YOUR_FILE_ID con el ID real del archivo   
          
    # Abre el PDF en una nueva pestaña
    #anvil.js.open_url(pdf_url)  # Esto abrirá la URL en una nueva pestaña
    
  def instrucciones_click(self, **event_args):
    # URL del PDF almacenado en Google Drive
    pdf_url = "https://drive.google.com/file/d/1uxMEnJ9On4-bYUBXRhzojsdq4EQSev2M/view?usp=sharing"  # Reemplaza YOUR_FILE_ID con el ID real del archivo     
          
    # Muestra una alerta con la URL del PDF
    alert(f"Puedes ver las instrucciones aquí: {pdf_url}")

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  #def link_6_click(self, **event_args):
    #"""This method is called when the link is clicked"""
    #pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
    