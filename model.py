import MySQLdb
#conexión coa bd
def obtener_conexion():
    return MySQLdb.connect(user='afd', password='afd', host='127.0.0.1', port=3306, database='CRUDclientes')

#funcións
def engadir_cliente(nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO Cliente (nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais))
            conexion.commit()
            print("Cliente engadido con éxito.")
        except Exception as e:
            conexion.rollback()
            print("Error ao engadir ó cliente:", e)
    conexion.close()


def obtener_clientes():
    conexion = obtener_conexion()
    clientes_data = []  # Utilizar un nombre más descriptivo para la variable
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais FROM Cliente ORDER BY id DESC ")
        rows = cursor.fetchall()
        # Construir una lista de diccionarios para los clientes
        for row in rows:
            cliente = {
                'id': row[0],
                'nombre': row[1],
                'apellidos': row[2],
                'email': row[3],
                'telefono': row[4],
                'sexo': row[5],
                'direccion': row[6],
                'ciudad': row[7],
                'pais': row[8]
            }
            clientes_data.append(cliente)
    conexion.close()
    return clientes_data


def obtener_cliente_por_id(id):
    conexion = obtener_conexion()
    Cliente = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais FROM Cliente WHERE id = %s", (id,))
        Cliente = cursor.fetchone()
    conexion.close()
    return Cliente

def actualizar_cliente(id, nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Cliente SET nombre = %s, apellidos = %s, email = %s, telefono = %s, sexo = %s, direccion = %s, ciudad = %s, pais = %s WHERE id = %s",
                       (nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais, id))
    
    conexion.commit()
    conexion.close()


def eliminar_cliente(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Cliente WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()
