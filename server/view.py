from flask import jsonify, request

from services.api_dati_ocr import WebApiOcr, WebApiTrain
from services.ocr_contains_label import OcrContainsLabel


def home():
    return jsonify({'status': 'success'})


def convert_file_to_text():
    content = WebApiOcr().run(request.files['file'])
    return jsonify({'status': 'success', 'content': content})


def train_machine_learning():
    content = WebApiTrain().run(request.data)
    return jsonify({'status': 'success', 'content': content})


def contains_label_in_archive():
    content = OcrContainsLabel(request.files['file']).run()
    return jsonify({'status': 'success', 'content': content})
