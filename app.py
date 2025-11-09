# En app.py, modifica la ruta /registro

# Necesitas importar jsonify
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import oracledb
# ... (el resto de tu setup) ...

# Crear la aplicación Flask (necesario antes de usar @app.route)
app = Flask(__name__)


@app.route("/")
def index():
    """Redirige la raíz a la página de registro"""
    return redirect(url_for('registro'))

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    """Maneja el registro de un nuevo Votante"""
    
    # Si es GET, solo muestra la plantilla HTML
    if request.method == 'GET':
        return render_template('registro.html')

    # Si es POST, procesa los datos JSON
    data = request.get_json() # Obtiene datos del fetch de JS
    if not data:
        return jsonify({"status": "error", "message": "Datos no recibidos."}), 400

    nombre = data.get('nombre')
    dni = data.get('dni')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    
    # (Validaciones y hasheo de contraseña irían aquí)

    try:
        with pool.acquire() as connection:
            cursor = connection.cursor()
            sql_insert = """
                INSERT INTO USUARIO (nombre, dni, correo, contraseña, rol)
                VALUES (:1, :2, :3, :4, 'VOTANTE')
            """
            cursor.execute(sql_insert, [nombre, dni, correo, contraseña])
            connection.commit()
            
            # Devuelve una respuesta JSON exitosa
            return jsonify({
                "status": "success", 
                "message": "¡Registro exitoso! Ya puedes iniciar sesión."
            }), 201

    except oracledb.DatabaseError as e:
        error_obj, = e.args
        if error_obj.code == 1: # Constraint única violada
            #
            message = 'Error: El DNI o el Correo ya existen.'
            if "CORREO" in error_obj.message.upper():
                message = 'El correo electrónico ya está registrado.'
            elif "DNI" in error_obj.message.upper():
                message = 'El DNI ya está registrado.'
            return jsonify({"status": "error", "message": message}), 409
        else:
            return jsonify({"status": "error", "message": f"Error de DB: {e}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error inesperado: {e}"}), 500


if __name__ == '__main__':
    # Arranca la aplicación en modo desarrollo cuando se ejecuta directamente
    app.run(host='127.0.0.1', port=5000, debug=True)