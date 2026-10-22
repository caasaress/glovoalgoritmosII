import sqlite3
from contextlib import closing

DB_PATH = "delivery.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with closing(get_conn()) as conn, conn:
        with open("delivery.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        with open("rutas.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())

def obtener_platos():
    with closing(get_conn()) as conn:
        return conn.execute("SELECT * FROM plato ORDER BY precio DESC").fetchall()

def obtener_riders():
    with closing(get_conn()) as conn:
        return conn.execute("SELECT nombre, barrio FROM rider WHERE barrio IS NOT NULL").fetchall()

def obtener_detalle_pedido(pedido_id):
    """Obtiene toda la información de un pedido mediante JOINs entre tablas relacionales."""
    with closing(get_conn()) as conn:
        query = """
            SELECT 
                p.id AS pedido_id,
                p.fecha,
                u.nombre AS cliente,
                u.barrio AS barrio_cliente,
                r.nombre AS rider,
                pl.nombre AS plato,
                pl.restaurante,
                pp.cantidad,
                pl.precio,
                (pp.cantidad * pl.precio) AS subtotal
            FROM pedido p
            JOIN usuario u ON p.usuario_id = u.id
            JOIN rider r ON p.rider_id = r.id
            JOIN pedido_plato pp ON p.id = pp.pedido_id
            JOIN plato pl ON pp.plato_id = pl.id
            WHERE p.id = ?
        """
        return conn.execute(query, (pedido_id,)).fetchall()