import json

from services.web_api_train.train.data_extractor import DataExtractor
from validators.validate_quantity_values import ValidateQuantityValues


class WebApiTrain:
    def run(self, request):
        data = json.loads(request.decode("UTF-8"))
        data_extractor = DataExtractor(data)
        values_selected_by_regex = data_extractor.run()

        validators = ValidateQuantityValues(data)
        values_selected_by_regex = validators.validate(values_selected_by_regex)

        return values_selected_by_regex

# {"name":"IE_000.pdf","part_numbers": [["366400"]], "quantities": [["17.280,00"]], "unit_prices": [["1,72000"]]}