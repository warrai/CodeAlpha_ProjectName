import sys
sys.path.insert(0, 'D:\\url_shortener\\libs')

from flask import Flask, request, redirect, jsonify, render_template
import random
import string
from database import init_db, save_url, get_original_url, get_all_urls

app = Flask(__name__)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    urls = get_all_urls()
    return render_template('index.html', urls=urls)

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'No URL provided'}), 400

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    short_code = generate_short_code()
    save_url(short_code, original_url)

    short_url = request.host_url + short_code
    return jsonify({'short_url': short_url, 'short_code': short_code})

@app.route('/<short_code>')
def redirect_url(short_code):
    original_url = get_original_url(short_code)
    if original_url:
        return redirect(original_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)