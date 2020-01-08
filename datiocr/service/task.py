from datiocr.enumerations.ocr_regex import Annotation
from datiocr.model.format_data import FormatData
from datiocr.service.aws_connect import ConnectionOCR
import re


class DatiOcr(ConnectionOCR):

    def __init__(self, s3_bucket_name, object_name):
        super().__init__(s3_bucket_name, object_name)

    def run(self):
        format_data = FormatData(self.object_name)
        response = ''
        text = ''

        self.start_job()
        if self.is_job_complete():
            response = self.get_job_results()
        for resultPage in response:
            for item in resultPage["Blocks"]:
                if item["BlockType"] == "LINE":
                    text = text + " " + item["Text"]
            # text = [text + " " + item["Text"] for item in resultPage["Blocks"] if item["BlockType"] == "LINE"]

        quantity = re.findall(Annotation.BRF_QUANTITY.value, text)
        material = re.findall(Annotation.BRF_MATERIAL.value, text)
        unit_price = re.findall(Annotation.BRF_UNIT_PRICE.value, text)

        entities = self.get_comprehend(text)

        if len(material) == 1:
            format_data.result_search([quantity, material, unit_price])

        else:
            for q in quantity:
                [quantity.remove(q) for entity in entities["Entities"] if q.strip() in entity['Text']]
            format_data.result_search([quantity, material, unit_price])

        return format_data.get_result_search()
