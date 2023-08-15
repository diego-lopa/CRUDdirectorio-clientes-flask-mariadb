from flask import Flask, render_template, request, redirect
import model
#para la API REST necesitamos importar JSON
import json

app = Flask(__name__)

#rutas
@app.route("/", methods=["GET", "POST"])
def cliente():
    clientes = model.obtener_clientes()

    # Buscador
    search_query = request.args.get('search', '').lower()
    _page = int(request.args.get('_page', 1))

    if search_query:
        clientes = [
            cliente for cliente in clientes if
            search_query in cliente['nombre'].lower() or
            search_query in cliente['apellidos'].lower() or
            search_query in cliente['ciudad'].lower() or
            search_query in cliente['pais'].lower()
        ]

            #Paxinado
    # Define o tamaño da páxina desexado
    PAGE_SIZE = 20
    
    # Calcular a paxinación
    num_clientes = len(clientes)
    num_pages = (num_clientes + PAGE_SIZE - 1) // PAGE_SIZE
    clientes_paginados = clientes[(_page - 1) * PAGE_SIZE:_page * PAGE_SIZE]

    # Calcular as páxinas para a paxinación
    start_page = max(1, (_page - 1) // 4 * 4 + 1)
    end_page = min(num_pages, (_page - 1) // 4 * 4 + 5)
    pages = range(start_page, end_page)
    
            #crear táboa paxinada
    # Renderizar a plantilla 'clientes.html' cos datos necesarios
    return render_template('clientes.html', clientes=clientes_paginados, pages=pages, _page=_page, num_pages=num_pages, search_query=search_query)


@app.route("/engadir_cliente", methods=["GET", "POST"])
def engadir_cliente():
    return render_template("formulario.html")

@app.route("/gardar_cliente", methods=["POST"])
def gardar_cliente():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    sexo = request.form["sexo"]
    direccion = request.form["direccion"]
    ciudad = request.form["ciudad"]
    pais = request.form["pais"]
    model.engadir_cliente(nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/")

@app.route("/obtener_cliente_por_id/<int:id>", methods=["GET"])
def obtener_cliente_por_id(id):
    # Obtener el cliente por ID
    cliente = model.obtener_cliente_por_id(id)
    return render_template("detalle_cliente.html", cliente=cliente)


@app.route("/actualizar_cliente/<int:id>", methods=["GET", "POST"])
def actualizar_cliente(id):
    if request.method == "POST":
        # Obtener los datos del cliente actualizado desde el formulario
        id = request.form["id"]
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        sexo = request.form["sexo"]
        direccion = request.form["direccion"]
        ciudad = request.form["ciudad"]
        pais = request.form["pais"]

        # Actualizar los datos del cliente en la base de datos
        cliente = model.actualizar_cliente(id, nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais)
        cliente = model.obtener_cliente_por_id(id)

        print("Cliente actualizado:", cliente) #control

        # Redireccionar a la página de detalles del cliente actualizado
        return render_template("detalle_cliente.html", cliente=cliente)
    else:
        # Obtener los datos del cliente desde la base de datos por su ID
        cliente = model.obtener_cliente_por_id(id)

        print("Cliente obtenido:", cliente) #control

        # Renderizar el formulario con los datos del cliente para su edición
        return render_template("formulario_actualizar.html", cliente=cliente)


@app.route("/eliminar_cliente", methods=[ "POST"])
def eliminar_cliente():
    model.eliminar_cliente(request.form["id"])
    return redirect("/")



#rutas da API REST:

@app.route("/api/clientes", methods =["GET", "POST"])
def api_clientes():
    if request.method == "GET": #Leer todos /GET
        clientes = model.obtener_clientes()  #select a la BD
        return json.dumps(clientes),200,{"Content-Type":"application/json"} #especificamos que es formato json
    
    elif request.method =="POST": #Crear /POST
        nombre = request.json["nombre"]
        apellidos = request.json["apellidos"]
        email = request.json["email"]
        telefono = request.json["telefono"]
        sexo = request.json["sexo"]
        direccion = request.json["direccion"]
        ciudad = request.json["ciudad"]
        pais = request.json["pais"]
        clientes = model.engadir_cliente(nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais)
        return json.dumps(clientes),201,{"Content-Type":"application/json"}
    
@app.route("/api/clientes/<int:id>", methods =["GET", "PUT", "DELETE"])
def api_clientesid(id):
    if request.method == "GET": # Leer uno /GET
        cliente = model.obtener_cliente_por_id(id)
        if cliente:
            return json.dumps(cliente), 200, {"Content-Type": "application/json"}
        else:
            return json.dumps({"message": "Non se atopou o cliente"}), 404, {"Content-Type": "application/json"}

    elif request.method == "DELETE": # Eliminar /DELETE
        resultado = model.eliminar_cliente(id)
        if resultado:
            return json.dumps({"message": "Cliente eliminado correctamente"}), 204, {"Content-Type": "application/json"}
        else:
            return json.dumps({"message": "Non se atopou o cliente"}), 404, {"Content-Type": "application/json"}

    elif request.method == "PUT": # Editar /PUT
        nombre = request.json.get("nombre")
        apellidos = request.json.get("apellidos")
        email = request.json.get("email")
        telefono = request.json.get("telefono")
        sexo = request.json.get("sexo")
        direccion = request.json.get("direccion")
        ciudad = request.json.get("ciudad")
        pais = request.json.get("pais")

        if any(value is not None for value in [nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais]):
            model.actualizar_cliente(id, nombre, apellidos, email, telefono, sexo, direccion, ciudad, pais)
            cliente_actualizado = model.obtener_cliente_por_id(id)
            if cliente_actualizado:
                return json.dumps({"message": "Cliente actualizado correctamente"}), 200, {"Content-Type": "application/json"}
            else:
                return json.dumps({"message": "Non se atopou o cliente"}), 404, {"Content-Type": "application/json"}
        else:
            return json.dumps({"message": "Requírense datos para actualizar"}), 400, {"Content-Type": "application/json"}


# Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True)
