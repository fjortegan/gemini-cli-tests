from flask import Flask, render_template, request, jsonify, session, flash
from werkzeug.utils import secure_filename
import os
import json
import csv
import secrets
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Asegurar que el directorio de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página principal con el formulario de carga"""
    alumnos = [
        {'nombre': 'Alumno prueba', 'id': 1},
        {'nombre': 'María García', 'id': 2},
        {'nombre': 'Juan Pérez', 'id': 3},
        {'nombre': 'Ana Rodríguez', 'id': 4},
    ]
    return render_template('index.html', alumnos=alumnos)

@app.route('/upload', methods=['POST'])
def upload_files():
    """Manejar la carga de archivos"""
    try:
        if 'clientes' not in request.files or 'consumos' not in request.files:
            return jsonify({
                'success': False, 
                'error': 'Se requieren ambos archivos (clientes y consumos)'
            })
        
        clientes_file = request.files['clientes']
        consumos_file = request.files['consumos']
        
        if clientes_file.filename == '' or consumos_file.filename == '':
            return jsonify({
                'success': False, 
                'error': 'No se han seleccionado archivos'
            })
        
        if not (allowed_file(clientes_file.filename) and allowed_file(consumos_file.filename)):
            return jsonify({
                'success': False, 
                'error': 'Solo se permiten archivos CSV y TXT'
            })
        
        # Generar timestamp único para esta carga
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Guardar archivos de clientes
        clientes_filename = secure_filename(f"{timestamp}_clientes_{clientes_file.filename}")
        clientes_path = os.path.join(app.config['UPLOAD_FOLDER'], clientes_filename)
        clientes_file.save(clientes_path)
        
        # Guardar archivo de consumos
        consumos_filename = secure_filename(f"{timestamp}_consumos_{consumos_file.filename}")
        consumos_path = os.path.join(app.config['UPLOAD_FOLDER'], consumos_filename)
        consumos_file.save(consumos_path)
        
        # Procesar archivos CSV (ejemplo básico)
        clientes_data = process_csv_file(clientes_path)
        consumos_data = process_csv_file(consumos_path)
        
        # Guardar información en sesión
        session['last_upload'] = {
            'clientes_file': clientes_filename,
            'consumos_file': consumos_filename,
            'timestamp': timestamp,
            'clientes_rows': len(clientes_data),
            'consumos_rows': len(consumos_data)
        }
        
        return jsonify({
            'success': True,
            'message': 'Archivos subidos y procesados exitosamente',
            'data': {
                'clientes_rows': len(clientes_data),
                'consumos_rows': len(consumos_data),
                'files': [clientes_filename, consumos_filename]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error durante la carga: {str(e)}'
        })

@app.route('/upload-progress', methods=['POST'])
def upload_progress():
    """Endpoint para actualizar el progreso de carga"""
    data = request.get_json()
    progress = data.get('progress', 0)
    current_file = data.get('file', '')
    
    # En una aplicación real, aquí se actualizaría el progreso real
    return jsonify({
        'progress': progress,
        'current_file': current_file,
        'status': 'uploading'
    })

@app.route('/results')
def results():
    """Mostrar resultados de la carga"""
    last_upload = session.get('last_upload')
    if not last_upload:
        flash('No hay datos de carga previos', 'warning')
        return render_template('results.html')
    
    return render_template('results.html', upload_data=last_upload)

@app.route('/validate-csv', methods=['POST'])
def validate_csv():
    """Validar archivos CSV antes de procesar"""
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Leer primeras líneas para validar
            csv_data = []
            for i, line in enumerate(file.stream):
                if i >= 5:  # Leer primeras 5 líneas
                    break
                csv_data.append(line.decode('utf-8').strip())
            
            return jsonify({
                'valid': True,
                'preview': csv_data[:3],  # Mostrar primeras 3 líneas
                'delimiter': detect_delimiter(csv_data[0]) if csv_data else ','
            })
        
        return jsonify({
            'valid': False,
            'error': 'Archivo no válido'
        })
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        })

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'success': False,
        'error': 'El archivo es demasiado grande. Máximo 16MB permitido.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

def process_csv_file(filepath):
    """Procesar archivo CSV y devolver datos"""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        print(f"Error procesando archivo {filepath}: {e}")
        # Intentar con latin-1
        try:
            with open(filepath, 'r', encoding='latin-1') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(row)
        except Exception as e:
            print(f"Error con latin-1 también: {e}")
            raise
    
    return data

def detect_delimiter(line):
    """Detectar delimitador CSV"""
    delimiters = [',', ';', '\t', '|']
    for delimiter in delimiters:
        if delimiter in line:
            return delimiter
    return ','

@app.context_processor
def utility_processor():
    """Funciones útiles disponibles en todas las plantillas"""
    def format_size(size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def get_file_extension(filename):
        return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    def format_datetime(dt_string):
        try:
            dt = datetime.strptime(dt_string, '%Y%m%d_%H%M%S')
            return dt.strftime('%d/%m/%Y %H:%M:%S')
        except:
            return dt_string
    
    return dict(
        format_size=format_size,
        get_file_extension=get_file_extension,
        format_datetime=format_datetime
    )

if __name__ == '__main__':
    # Asegurarse de que existe el directorio uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Ejecutar en modo debug para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)