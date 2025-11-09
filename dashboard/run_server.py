from flask import Flask, send_from_directory, jsonify
import os
import json

app = Flask(__name__, static_folder='.', static_url_path='')

# Caminho do arquivo JSON (ajuste se necessário)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')


@app.route('/')
def index():
    """Serve o index.html"""
    return send_from_directory('.', 'index.html')


@app.route('/data')
def get_data():
    """Serve o conteúdo do data.json como JSON"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/<path:path>')
def serve_static(path):
    """Serve outros arquivos estáticos (CSS, JS, imagens, etc.)"""
    return send_from_directory('.', path)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
