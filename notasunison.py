from flask import Flask, render_template, request, redirect, url_for, flash
# Importa init_db y get_connection
from ConexionBD.conexion import init_db, get_connection
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para mostrar mensajes flash

# =========================
# Rutas de inicio
# =========================


@app.route('/')
@app.route('/index')
def inicio():
    return render_template('inicio.html')

# =========================
# Ruta para crear una nota
# =========================


@app.route('/crear_nota', methods=['GET', 'POST'])
def crear_nota():
    mensaje = ""
    try:
        init_db()  # Inicializamos la base de datos y creamos la tabla si no existe
        mensaje = "Conexión exitosa a la base de datos"
    except sqlite3.Error as e:
        mensaje = f"Error al conectar a la base de datos: {e}"

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']

        try:
            conexion = get_connection()  # Usamos la función central para conectarnos
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO notas (titulo, descripcion, fecha) VALUES (?, ?, ?)",
                (titulo, descripcion, fecha)
            )

            conexion.commit()
            conexion.close()

            flash("Nota agregada correctamente", "success")
            return redirect(url_for('listar_notas'))

        except sqlite3.Error as e:
            flash(f"Error al guardar la nota: {e}", "danger")
            return redirect(url_for('crear_nota'))

    return render_template('crear_nota.html', mensaje=mensaje)

# =========================
# Ruta para listar notas
# =========================


@app.route('/listar_notas')
def listar_notas():
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, titulo, descripcion, fecha FROM notas")
        notas = cursor.fetchall()
        conexion.close()
    except sqlite3.Error as e:
        flash(f"Error al leer las notas: {e}", "danger")
        notas = []

    return render_template('listar_notas.html', notas=notas)

# =========================
# Ruta para modificar una nota
# =========================


@app.route('/modificar_nota/<int:nota_id>', methods=['GET', 'POST'])
def modificar_nota(nota_id):
    if request.method == 'POST':
        # Recibimos los datos modificados
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']

        try:
            conexion = sqlite3.connect('ConexionBD/notas.db')
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE notas SET titulo=?, descripcion=?, fecha=? WHERE id=?",
                (titulo, descripcion, fecha, nota_id)
            )
            conexion.commit()
            conexion.close()
            flash("Nota modificada correctamente", "success")
            return redirect(url_for('listar_notas'))
        except sqlite3.Error as e:
            flash(f"Error al modificar la nota: {e}", "danger")
            return redirect(url_for('modificar_nota', nota_id=nota_id))

    else:
        # GET: obtener los datos de la nota para mostrar en el formulario
        try:
            conexion = sqlite3.connect('ConexionBD/notas.db')
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM notas WHERE id=?", (nota_id,))
            nota = cursor.fetchone()
            conexion.close()
        except sqlite3.Error as e:
            flash(f"Error al obtener la nota: {e}", "danger")
            return redirect(url_for('listar_notas'))

        if nota is None:
            flash("Nota no encontrada", "warning")
            return redirect(url_for('listar_notas'))

        return render_template('modificar_nota.html', nota=nota)


# =========================
# Ruta para eliminar una nota
# =========================


@app.route('/eliminar_nota/<int:nota_id>', methods=['POST'])
def eliminar_nota(nota_id):
    try:
        conexion = sqlite3.connect('ConexionBD/notas.db')
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM notas WHERE id=?", (nota_id,))
        conexion.commit()
        conexion.close()
        flash("Nota eliminada correctamente", "success")
    except sqlite3.Error as e:
        flash(f"Error al eliminar la nota: {e}", "danger")
    return redirect(url_for('listar_notas'))


# =========================
# Ejecución de la app
# =========================
if __name__ == '__main__':
    app.run(debug=True)
