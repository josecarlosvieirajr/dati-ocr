import json

import redis

from services.web_api_ocr.ocr.general_ocr.services.ocr_connect import ConnectOcr
from services.web_api_ocr.ocr.general_ocr.services.ocr_find_table import FindTableOCR
from services.web_api_ocr.ocr.general_ocr.services.ocr_find_table2 import FindTableOCR2

db = redis.Redis()


class GeneralOCR(ConnectOcr):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.data = None
        self.file = None

    def run(self, file):
        self.file = file
        if self.ocr_di_data():
            # table = FindTableOCR(self.data).run()
            df = FindTableOCR2(self.data).run()
            df.to_pickle(f"./dummy_{file.filename}.pkl")
            return self.new_general_ocr()
        return False

    def ocr_di_data(self):
        if self.upload_file(self.file):
            self.data = self.ocr_object()
            self.delete_object_s3()
            return True
        return False

    def new_general_ocr(self):
        size = 100
        front_table = []
        for item in self.data['Blocks']:
            if item["BlockType"] == "LINE":
                front_table.append([
                    item['Text'],
                    item['Geometry']['BoundingBox']['Width'] * size,
                    item['Geometry']['BoundingBox']['Height'] * size * 2.5,
                    item['Geometry']['BoundingBox']['Left'] * size,
                    item['Geometry']['BoundingBox']['Top'] * size * 2.3 * (item['Page'] * 3),
                ])
        return front_table
