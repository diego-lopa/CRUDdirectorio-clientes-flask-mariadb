Aplicación web de xestión de clientes CRUD.

# Esta é unha aplicación web desenvolvida con Flask para a xestión de clientes a partir dunha base de datos mariadb.
Permítelle aos usuarios visualizar de forma ordenada o conxunto de usurios presentados nunha táboa paxinada cuns cadros de "Nome e apelidos", "Cidade" e "País", un buscador con eses datos así como a opción de engadir novo cliente, que dirixe a un formulario de creación. Ao facerlle clic ao nome ou apelidos de cada cliente lévate a outra páxina na que se mostran todos os datos da persoa, na que se poden modificar os datos do cliente ou eliminalo.
# Esructura
A aplicación está estructurada mediante o modelo vista controlador (MVC)
- No `model.py` impórtase a base de datos mariadb e contén as funcións para mostrar, crear, actualizar e eliminar.
- O `app.py` é o controlador do programa, onde as rutas ('/'), ("/engadir_cliente"), ("/gardar_cliente"), ("/obtener_cliente_por_id/<int:id>"), ("/actualizar_cliente/<int:id>"), ("/eliminar_cliente") encárganse de adaptar a información para que se lle mostre ao usuario mediante as vistas.
- O cartafol de `templates` contén os arquivos .html divididos en `base.html` están os estilos css común ao resto dos arquivos, a barra de navegación ca opción de engadir e a estructura da páxina. No `clientes.html` atópase a táboa onde se mostran, a opción de eliminar e a e paxinación. No `detalle_cliente.html` móstrase unha lista cos datos de cade cliente, un botón para modificar os datos e outro para eliminalo. Os `formulario.html` e `formulario_actualizar.html` son os formularios de creación e modificación de clientes.

# Requisitos
- Python 3.x
- Flask
- wsl
- MySQLdb

# Posta en marcha
1. Crea e activa un entorno virtual (opcional pero recomendado):
python3 -m venv venv
source venv/bin/activate

2. Instala as dependencias:
pip install -r requirements.txt

3. Conectese a base de datos mariadb:
1º WSL:
[terminal]:
        wsl --install -d Debian
	    $ sudo apt update
	
2ºMariaDB:
[terminal]:
        $ sudo apt install mariadb-server
	    $ sudo service mariadb start
	    $ sudo mariadb

4. Inicia a aplicación:
python app.py

5. Abre o teu navegador web e visita http://localhost:5000 para acceder á aplicación.

# Uso
- Na páxina principal, atoparás unha táboa paxinada cuns cadros de "Nome e apelidos", "Cidade" e "País".
- Mediante o buscador filtrarase os clientes que conteñan no seu nome, apelido, cidade ou pais o termo a buscar.
- Cada cliente contará cunha lista completa dos seus datos accesible mediante un clic no nome ou apelido.