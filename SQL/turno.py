from contextlib import closing
from db import get_conn

def planificar_turno():
    with closing(get_conn()) as conn:
        repartos = conn.execute("SELECT * FROM reparto ORDER BY fin ASC").fetchall()
        
    seleccionados = []
    fin_ultimo = "00:00"
    
    for r in repartos:
        if r["inicio"] >= fin_ultimo:
            seleccionados.append(dict(r))
            fin_ultimo = r["fin"]
            
    return seleccionados