from contextlib import closing
from db import get_conn

def crear_pedido(usuario_id, rider_id, lineas, fecha):
    with closing(get_conn()) as conn, conn:
        cur = conn.execute(
            "INSERT INTO pedido (fecha, usuario_id, rider_id) VALUES (?, ?, ?)", 
            (fecha, usuario_id, rider_id)
        )
        pedido_id = cur.lastrowid
        
        lineas_con_id = [(pedido_id, plato_id, cantidad) for plato_id, cantidad in lineas]
        conn.executemany(
            "INSERT INTO pedido_plato (pedido_id, plato_id, cantidad) VALUES (?, ?, ?)", 
            lineas_con_id
        )
        
        total = 0
        for plato_id, cantidad in lineas:
            plato = conn.execute("SELECT precio FROM plato WHERE id = ?", (plato_id,)).fetchone()
            if plato:
                total += plato["precio"] * cantidad
                
        usuario = conn.execute("SELECT saldo FROM usuario WHERE id = ?", (usuario_id,)).fetchone()
        if not usuario or usuario["saldo"] < total:
            raise ValueError("Tarjeta rechazada: saldo insuficiente")
            
        conn.execute("UPDATE usuario SET saldo = saldo - ? WHERE id = ?", (total, usuario_id))
        
        return pedido_id, total