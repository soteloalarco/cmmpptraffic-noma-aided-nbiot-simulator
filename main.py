from des import sim

config_Archivo="config.json" # Nombre del archivo de configuración
config_Seccion="simulacion" # Nombre de la sección de donde se leerán los parámetros para configurar el simulador
Opcion_run=0

simulator = sim.Sim.Instance()
simulator.set_config(config_Archivo, config_Seccion)
simulator.initialize(Opcion_run)
simulator.run()