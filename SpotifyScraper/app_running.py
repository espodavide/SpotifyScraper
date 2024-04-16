from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import render_template
from flask import send_file
import json
from flask_cors import CORS
import io
import zipfile
import time
import logging
import os

# Configura il logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from SpotifyScraper import *
from YoutubeToMp3 import *


# Verifica la connessione Internet all'interno del container Docker
import requests

def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

if not check_internet_connection():
    logging.warning("Errore: Connessione Internet non disponibile.")
else:
    logging.warning("Connessione Internet OK.")



app = Flask(__name__)
CORS(app)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error('An error occurred: %s', str(e))
    return 'An internal server error occurred', 500


@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')

@app.route('/test', methods=['GET'])
def test():
    return "Everything is working fine"


@app.route('/scrapingDownload', methods=['POST'])
def scraping():
    if request.method =='POST':
        content = request.json
        url =content['url']
        print(url)
        print(f'Running scraping on spotify')
        playlist_name = SpotifyScraper(url)
        print(f'Downloading the playlist')
        zip_file_path = YoutubeToMp3(playlist_name)
        print("Sending zip file to the final user... ", zip_file_path)

        FILEPATH = zip_file_path
        print(FILEPATH)
        fileobj = io.BytesIO()
        with zipfile.ZipFile(fileobj, 'w') as zip_file:
            zip_info = zipfile.ZipInfo(FILEPATH)
            zip_info.date_time = time.localtime(time.time())[:6]
            zip_info.compress_type = zipfile.ZIP_DEFLATED
            with open(FILEPATH, 'rb') as fd:
                zip_file.writestr(zip_info, fd.read())
        fileobj.seek(0)

        return send_file(FILEPATH, as_attachment=True)

    else:
        return 'This method is not allowed', 400

if __name__ == '__main__':
    PORT = int(os.environ.get("containerPort",8080))
    if PORT != 8080:
        PORT = int(os.environ.get("PORT",8080))
    app.run(host='0.0.0.0',port=int(PORT),debug=True)