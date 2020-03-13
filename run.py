from flask import Flask, request, jsonify
from services.api_dati_ocr import WebApiOcr, WebApiTrain

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'success'})


@app.route('/send_ocr_file', methods=['POST'])
def convert_file_to_text():
    content = WebApiOcr().run(request.files['file'])
    return jsonify({'status': 'success', 'content': content})


@app.route('/send_data_selected', methods=['POST'])
def train_machine_learning():
    content = WebApiTrain().run(request.data)
    return jsonify({'status': 'success', 'content': content})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=False, debug=True)
