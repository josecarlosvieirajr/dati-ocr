import json
import redis

from services.ocr.data_extractor import DataExtractor
from services.ocr.general_ocr import GeneralOCR

db = redis.Redis()


class WebApiOcr:
    def __init__(self):
        self.values = None

    def run(self, file):
        self.values = GeneralOCR().run(file)
        for i in self.values:
            db.lpush('base', i[0])
        return self.values


class WebApiTrain:
    def run(self, request):
        data = json.loads(request.decode("UTF-8"))
        data_extractor = DataExtractor(data)
        values_selected_by_regex = data_extractor.run()

        return values_selected_by_regex

# {"part_numbers": ["366400"], "quantities": ["17.280,00"], "unit_prices": ["1,72000"]}
