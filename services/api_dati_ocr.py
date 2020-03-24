import json
import redis

from services.ocr.data_extractor import DataExtractor
from services.ocr.general_ocr import GeneralOCR
from validators.validate_quantity_values import ValidateQuantityValues

db = redis.Redis()


class WebApiOcr:
    def __init__(self):
        self.values = None

    def run(self, file):
        self.values = GeneralOCR().run(file)
        for i in self.values:
            db.lpush(f'base_{file.filename}', i[0])
            db.lpush(i[0], f"{i[1]} | {i[2]} | {i[3]} | {i[4]}")
        return self.values


class WebApiTrain:
    def run(self, request):
        data = json.loads(request.decode("UTF-8"))
        data_extractor = DataExtractor(data)
        values_selected_by_regex = data_extractor.run()

        validators = ValidateQuantityValues(data)
        validators.validate(values_selected_by_regex)

        return validators.get_values()
        # return values_selected_by_regex

# {"name":"IE_000.pdf","part_numbers": [["366400"]], "quantities": [["17.280,00"]], "unit_prices": [["1,72000"]]}
