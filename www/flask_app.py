import requests
from theimage import ThermoImage
from flask import Flask, request

tg_url = 'https://api.telegram.org'
app = Flask(__name__)


@app.route('/bot<token>/<file_id>', methods=['POST'])
def download_from_telegram(token, file_id):
    content = request.json
    if isinstance(content, list) and len(content) == 4:
        chat = str(content[0])
        name = str(content[1])
        text = str(content[2])
        r = requests.post(f'{tg_url}/bot{token}/getFile',
                          json={'file_id': file_id, 'chat_id': chat})
        if r.ok:
            file_path = r.json()['result']['file_path']
            r = requests.get(f'{tg_url}/file/bot{token}/{file_path}')
            if r.ok:
                image = ThermoImage(r.content)
                image.instagram(name, text)
                return image.binary
    return ''
