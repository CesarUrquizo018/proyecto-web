from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MYSQL conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306 # Puerto del servidor MySQL
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'solicitudes'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html',clientes = data)

@app.route('/add_cliente', methods=['POST'])
def add_clientes():
    if request.method =='POST':
        numerosolicitud = request.form['numerosolicitud']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        celular = request.form['celular']
        direccion = request.form['direccion']
        fechainicio = request.form['fechainicio']
        estado = request.form['estado']
        actualizacion = request.form['actualizacion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes(numerosolicitud, nombre, apellido, correo, celular, direccion, fechainicio, estado, actualizacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (numerosolicitud, nombre, apellido, correo, celular, direccion, fechainicio, estado, actualizacion))
        mysql.connection.commit()
        flash('Cliente Agregado satisfactoriamente')

        return redirect(url_for('Index'))



@app.route('/edit/<idcliente>')
def get_clientes(idcliente):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE idcliente = %s', (idcliente))
    data = cur.fetchall()
    return render_template('edit-clientes.html', cliente=data[0])

@app.route('/update/<idcliente>', methods=['POST'])
def update_clientes(idcliente):
    if request.method == 'POST':
        numerosolicitud = request.form['numerosolicitud']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        celular = request.form['celular']
        direccion = request.form['direccion']
        fechainicio = request.form['fechainicio']
        estado = request.form['estado']
        actualizacion = request.form['actualizacion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET numerosolicitud = %s,
                nombre = %s,
                apellido = %s,
                correo = %s,
                celular = %s,
                direccion = %s,
                fechainicio = %s,
                estado = %s,
                actualizacion = %s
            WHERE idcliente = %s
        """, (numerosolicitud, nombre, apellido, correo, celular, direccion, fechainicio, estado, actualizacion, idcliente))
        flash('Cliente Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<idcliente>')
def delete_clientes(idcliente):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE idcliente = {0}'.format(idcliente))
    mysql.connection.commit()
    flash('Clientes Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)