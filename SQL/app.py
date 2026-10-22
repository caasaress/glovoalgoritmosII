import sqlite3
from db import obtener_platos
from pedidos import crear_pedido
from rutas import cargar_grafo, calcular_ruta_optima, rider_mas_cercano
from turno import planificar_turno

def ver_carta():
    print("\n--- CARTA DE PLATOS ---")
    for p in obtener_platos():
        print(f"- {p['nombre']} ({p['restaurante']}) [{p['categoria']}]: {p['precio']}€")

def pedir(grafo):
    u_id = int(input("Id de usuario: "))
    r_id = int(input("Id de rider: "))
    fecha_es = input("Fecha (DD-MM-YYYY): ")
    partes = fecha_es.split("-")
    fecha = f"{partes[2]}-{partes[1]}-{partes[0]}" if len(partes) == 3 else fecha_es
    
    print("\n--- CARTA DE PLATOS DISPONIBLES ---")
    platos_disponibles = obtener_platos()
    for p in platos_disponibles:
        print(f"ID [{p['id']}] - {p['nombre']} ({p['restaurante']}): {p['precio']}€")
        
    lineas = []
    
    while True:
        plato_id = int(input("\nIntroduce el ID del plato que deseas: "))
        cantidad = int(input("Cantidad: "))
        lineas.append((plato_id, cantidad))
        
        continuar = input("¿Deseas pedir algún plato más? (s/n): ").strip().lower()
        if continuar != 's':
            break
            
    conn = sqlite3.connect("delivery.db")
    conn.row_factory = sqlite3.Row
    total_estimado = 0
    resumen_texto = []
    
    for plato_id, cantidad in lineas:
        plato = conn.execute("SELECT * FROM plato WHERE id = ?", (plato_id,)).fetchone()
        if plato:
            subtotal = plato["precio"] * cantidad
            total_estimado += subtotal
            resumen_texto.append(f"- {cantidad}x {plato['nombre']} ({plato['restaurante']}): {subtotal}€")
    conn.close()
    
    print("\n--- RESUMEN DEL PEDIDO ---")
    for r in resumen_texto:
        print(r)
    print(f"Total estimado: {total_estimado}€")
    
    confirma = input("¿Deseas confirmar el pedido? (s/n): ").strip().lower()
    if confirma != 's':
        print("Pedido cancelado.")
        return

    try:
        pid, total = crear_pedido(u_id, r_id, lineas, fecha)
        print(f"¡Pedido creado con éxito! ID de pedido: {pid} | Total cobrado: {total}€")
    except ValueError as e:
        print(e)

def asignar(grafo):
    while True:
        print("\n--- BARRIOS DISPONIBLES ---")
        for b in grafo.keys():
            print(f"- {b}")
            
        entrada = input("\nIntroduce el barrio del restaurante: ").strip()
        
        # Buscamos ignorando mayúsculas/minúsculas comparando el lower()
        barrio_encontrado = None
        for b in grafo.keys():
            if b.lower() == entrada.lower():
                barrio_encontrado = b
                break
                
        if barrio_encontrado:
            minutos, nombre = rider_mas_cercano(grafo, barrio_encontrado)
            print(f"El rider más cercano es {nombre} a {minutos} minutos del restaurante.\n")
            break
        else:
            print("El barrio no existe o está mal escrito. Vuelve a intentarlo.")

def ruta(grafo):
    while True:
        print("\n--- BARRIOS DISPONIBLES ---")
        for b in grafo.keys():
            print(f"- {b}")
            
        entrada_origen = input("\nIntroduce el barrio de origen: ").strip()
        origen_encontrado = None
        for b in grafo.keys():
            if b.lower() == entrada_origen.lower():
                origen_encontrado = b
                break
                
        entrada_destino = input("Introduce el barrio de destino: ").strip()
        destino_encontrado = None
        for b in grafo.keys():
            if b.lower() == entrada_destino.lower():
                destino_encontrado = b
                break
                
        if origen_encontrado and destino_encontrado:
            minutos, cam = calcular_ruta_optima(grafo, origen_encontrado, destino_encontrado)
            print(f"\nDistancia: {minutos} min, Ruta: {cam}\n")
            break
        else:
            print("Algún barrio introducido no existe o está mal escrito. Vuelve a intentarlo.")

def mostrar_turno():
    repartos = planificar_turno()
    print("\n--- REPARTOS SELECCIONADOS (TURNO ÓPTIMO) ---")
    for r in repartos:
        print(f"Zona: {r['zona']} | De {r['inicio']} a {r['fin']}")
    print()

def main():
    ""
    grafo = cargar_grafo()
    opciones = {
        "1": ("Ver la carta",           ver_carta),
        "2": ("Hacer un pedido",        lambda: pedir(grafo)),
        "3": ("Rider para un pedido",   lambda: asignar(grafo)),
        "4": ("Ruta entre dos barrios", lambda: ruta(grafo)),
        "5": ("Planificar el turno",    mostrar_turno),
    }
    while True:
        for k, (texto, _) in opciones.items():
            print(k, texto)
        eleccion = input("Opción (q para salir): ")
        if eleccion.lower() == "q":
            break
        opciones.get(eleccion, ("", lambda: print("No existe")))[1]()

if __name__ == "__main__":
    main()