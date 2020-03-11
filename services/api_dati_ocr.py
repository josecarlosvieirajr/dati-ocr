import json

from services.ocr.general_ocr import GeneralOCR


class WebApiOcr:
    def __init__(self):
        self.values = None

    def run(self, file):
        self.values = GeneralOCR().run(file)
        return self.values


class WebApiTrain:
    def run(self, request):
        print(request)
