

# from db import obtener_platos
# from pedidos import crear_pedido
from metodos_nuevos_sql import cargar_grafo, dijkstra, camino, rider_mas_cercano
# from turno import planificar_turno

def pedir(grafo):
    print("Funcionalidad de pedir en construcción...")

def asignar(grafo):
    barrio_rest = input("Dime el barrio del restaurante: ")
    if barrio_rest in grafo:
        minutos, rider = rider_mas_cercano(grafo, barrio_rest)
        print(f"El rider más cercano es {rider}, a {minutos} minutos.")
    else:
        print("Barrio no encontrado.")

def ruta(grafo):
    origen = input("Barrio origen: ")
    destino = input("Barrio destino: ")
    if origen in grafo and destino in grafo:
        dist, previo = dijkstra(grafo, origen)
        ruta_optima = camino(previo, destino)
        print(f"Ruta: {' -> '.join(ruta_optima)} ({dist[destino]} minutos)")
    else:
        print("Barrios no válidos.")

def main():
    grafo = cargar_grafo()
    
    opciones = {
        "1": ("Ver la carta", lambda: print("Carta... (importar de db.py)")),
        "2": ("Hacer un pedido", lambda: pedir(grafo)),
        "3": ("Rider para un pedido", lambda: asignar(grafo)),
        "4": ("Ruta entre dos barrios", lambda: ruta(grafo)),
        "5": ("Planificar el turno", lambda: print("Turno... (importar de turno.py)")),
    }
    
    while True:
        for k, (texto, _) in opciones.items():
            print(f"{k}. {texto}")
            
        eleccion = input("Opción (q para salir): ")
        if eleccion.lower() == "q":
            break
            
        accion = opciones.get(eleccion, ("", lambda: print("Opción no existe")))[1]
        accion()

