from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from contextlib import contextmanager
import io
import threading
from queue import Queue

posicao_nome = 1150
posicao_curso = 920
posicao_data = 1270
fonte = 'Inter.ttf'
tamanho_fonte = 60

data_desejada = datetime.now()
data_formatada = data_desejada.strftime("%d de %B de %Y")

app = Flask(__name__, template_folder='template')
output_queue = Queue()

@contextmanager
def create_bytesio():
    buffer = io.BytesIO()
    try:
        yield buffer
    finally:
        pass  # Não fechar o buffer aqui

def generate_certificate(nome, curso, template):
    with create_bytesio() as buffer:
        img = Image.open(template)
        font = ImageFont.truetype(fonte, size=tamanho_fonte)
        draw = ImageDraw.Draw(img)
        nome_pos = (img.width / 3, posicao_nome)
        date_pos = (img.width / 2.7, posicao_data)
        course_pos = (img.width / 1.47, posicao_curso)
        draw.text(nome_pos, nome, fill=(0, 0, 0), font=font, anchor="mm")
        draw.text(course_pos, curso, fill=(0, 0, 0), font=font, anchor="mm")
        draw.text(date_pos, data_formatada, fill=(0, 0, 0), font=font, anchor="mm")
        img.save(buffer, format="PNG")

    buffer.seek(0)
    return buffer.getvalue()

def gerar_certificado_thread(nome, curso):
    certificado = generate_certificate(nome, curso, 'modelo.png')
    output_queue.put(certificado)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/certificado', methods=['GET'])
def certificado():
    return render_template('certificado.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/mostrar-certificado', methods=['GET', 'POST'])
def gerar_certificado():
    nome = request.form['nome']
    curso = request.form['curso']
    thread = threading.Thread(target=gerar_certificado_thread, args=(nome, curso))
    thread.start()
    thread.join()
    certificado = output_queue.get()
    return send_file(io.BytesIO(certificado), mimetype="image/png")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
