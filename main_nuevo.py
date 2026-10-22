

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
    
    while True:
        print("1. Ver la carta")
        print("2. Hacer un pedido")
        print("3. Rider para un pedido")
        print("4. Ruta entre dos barrios")
        print("5. Planificar el turno")
            
        eleccion = input("Opción (q para salir): ")
        
        if eleccion.lower() == "q":
            break
        elif eleccion == "1":
            print("Carta... (importar de db.py)")
        elif eleccion == "2":
            pedir(grafo)
        elif eleccion == "3":
            asignar(grafo)
        elif eleccion == "4":
            ruta(grafo)
        elif eleccion == "5":
            print("Turno... (importar de turno.py)")
        else:
            print("Opción no existe")

