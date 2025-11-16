import sqlite3  # Importa SQLite para manejar la base de datos

# Función para obtener una conexión a la base de datos


def get_connection():
    """
    Retorna un objeto de conexión a la base de datos ConexionBD/notas.db.
    Si no existe, SQLite la crea automáticamente.
    """
    conn = sqlite3.connect(
        'ConexionBD/notas.db')  # Conecta a la BD dentro de la carpeta ConexionBD
    # Permite acceder a las filas como diccionarios
    conn.row_factory = sqlite3.Row
    return conn

# Función para inicializar la tabla 'notas' si no existe


def init_db():
    """
    Crea la tabla 'notas' si aún no existe.
    """
    conn = get_connection()  # Obtiene la conexión
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único y autoincrementable
            titulo TEXT NOT NULL,                   -- Título de la nota
            descripcion TEXT NOT NULL,              -- Contenido de la nota
            fecha TEXT NOT NULL                     -- Fecha de la nota
        )
    ''')
    conn.commit()  # Guarda los cambios
    conn.close()   # Cierra la conexión
