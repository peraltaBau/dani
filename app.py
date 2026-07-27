from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dany_cumple_18_2026'

# Configuración de imágenes
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'avif'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB (para videos)
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['VIDEO_FOLDER'] = 'static/videos/'

# Extensiones permitidas para videos
app.config['ALLOWED_VIDEO_EXTENSIONS'] = {'mp4', 'webm', 'ogg', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_VIDEO_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    video_mensaje = None
    
    # Fecha del cumpleaños: 17 de agosto de 2026
    fecha_cumple = datetime(2026, 8, 17, 0, 0, 0)
    fecha_actual = datetime.now()
    
    # Verificar si ya es el cumpleaños
    es_cumple = fecha_actual >= fecha_cumple
    
    # Calcular días restantes
    if not es_cumple:
        dias_restantes = (fecha_cumple - fecha_actual).days
    else:
        dias_restantes = 0
    
    # Subir imágenes
    if request.method == 'POST':
        # Subir imagen
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                mensaje = "🎉 ¡Imagen subida con éxito! 📸"
        
        # Subir video
        if 'video' in request.files:
            file = request.files['video']
            if file and allowed_video(file.filename):
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                file.save(os.path.join(app.config['VIDEO_FOLDER'], new_filename))
                video_mensaje = "🎬 ¡Video subido con éxito! 🎥"
    
    # Lista de imágenes para la galería
    imagenes = [
        'perfil.jpeg',
        'cumple1.jpeg',
        'cumple2.jpeg',
        'cumple3.jpeg',
        'cumple4.jpeg'
    ]
    
    # Lista de videos para la galería
    videos = [
        'video1.mp4',
        'video2.mp4',
        'video3.mp4',
        'video4.mp4'
    ]
    
    return render_template('index.html', 
                         mensaje=mensaje,
                         video_mensaje=video_mensaje,
                         imagenes=imagenes,
                         videos=videos,
                         es_cumple=es_cumple,
                         dias_restantes=dias_restantes,
                         fecha_cumple=fecha_cumple.strftime('%d de %B de %Y'))

# Ruta para servir videos
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)

# Crear carpetas si no existen
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/videos', exist_ok=True)
os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)