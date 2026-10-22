
import sqlite3
import heapq
from contextlib import closing

# Asumimos que db.py tiene una función similar, la definimos aquí por simplicidad
def get_conn():
    conn = sqlite3.connect("rider_express.db")
    conn.row_factory = sqlite3.Row
    return conn

def cargar_grafo():
    """{barrio: {vecino: minutos}} a partir de la tabla tramo."""
    grafo = {}
    with closing(get_conn()) as conn:
        for t in conn.execute("SELECT origen, destino, minutos FROM tramo"):
            grafo.setdefault(t["origen"], {})[t["destino"]] = t["minutos"]
            grafo.setdefault(t["destino"], {})[t["origen"]] = t["minutos"]
    return grafo

def dijkstra(grafo, origen):
    dist = {nodo: float("inf") for nodo in grafo}
    previo = {origen: None}
    dist[origen] = 0
    cola = [(0, origen)]
    cerrados = set()
    
    while cola:
        d, u = heapq.heappop(cola)
        if u in cerrados:
            continue
        cerrados.add(u)
        
        for v, peso in grafo[u].items():
            if d + peso < dist[v]:
                dist[v] = d + peso
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))
                
    return dist, previo

def camino(previo, destino):
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = previo.get(destino)
    return ruta[::-1]

def rider_mas_cercano(grafo, barrio_restaurante):
    dist = dijkstra(grafo, barrio_restaurante)
    with closing(get_conn()) as conn:
        riders = conn.execute(
            "SELECT nombre, barrio FROM rider WHERE barrio IS NOT NULL"
        ).fetchall()
    # Retorna tupla (minutos, nombre_rider)
    return min((dist[r["barrio"]], r["nombre"]) for r in riders)



