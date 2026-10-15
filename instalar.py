
import sqlite3
conexion = sqlite3.connect("rider_express")
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS Usuario")
cursor.execute("CREATE TABLE Usuario (id INTEGER PRIMARY KEY, name TEXT, birthday DATE)")
cursor.execute("DROP TABLE IF EXISTS Rider")
cursor.execute("CREATE TABLE Rider (id INTEGER PRIMARY KEY, name TEXT, id_vehiculo INTEGER)")
cursor.execute("DROP TABLE IF EXISTS Pedido")
cursor.execute("CREATE TABLE Pedido (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("DROP TABLE IF EXISTS Categoria_Restaurante")
cursor.execute("CREATE TABLE Categoria_Restaurante (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("DROP TABLE IF EXISTS Vehiculo")
cursor.execute("CREATE TABLE Vehiculo (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("DROP TABLE IF EXISTS Plato")
cursor.execute("CREATE TABLE Plato (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
cursor.execute("CREATE TABLE Pedido_Plato (id_plato INTEGER, id_pedido INTEGER, quantity INTEGER)")

conexion.commit()