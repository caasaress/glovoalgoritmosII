import heapq
from contextlib import closing
from db import get_conn, obtener_riders

def cargar_grafo():
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
        destino = previo[destino]
    return ruta[::-1]

def rider_mas_cercano(grafo, barrio_restaurante):
    dist, _ = dijkstra(grafo, barrio_restaurante)
    riders = obtener_riders()
    return min((dist[r["barrio"]], r["nombre"]) for r in riders)

def calcular_ruta_optima(grafo, origen, destino):
    dist, previo = dijkstra(grafo, origen)
    cam = camino(previo, destino)
    return dist[destino], cam