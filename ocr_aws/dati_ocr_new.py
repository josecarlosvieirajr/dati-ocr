from datiocr.enumerations.enum_test import EnumTeste
from datiocr.service.task import DatiOcr
from ocr_aws.test_ocr_new import TratamentoOCR


class GeneralOCR:
    @staticmethod
    def run():


        bucket = "ocrdatidev"
        doc = 'IE_000.pdf'
        top = DatiOcr(bucket, doc)
        response = top.run()
        # return TratamentoOCR(EnumTeste.LISTA_TESTE.value).format()
        return TratamentoOCR(response).format()
        # lista_pages = []
        # geral = []
        # arrayzao = {}
        #
        # for item in response["Blocks"]:
        #     if item['Page'] not in lista_pages:
        #         lista_pages.append(item['Page'])
        #
        # for val in lista_pages:
        #     for item in response["Blocks"]:
        #         if item["BlockType"] == "LINE" and item['Page'] == val:
        #             geral.append([
        #                 item['Text'],
        #                 item['Geometry']['BoundingBox']['Width'] * 100,
        #                 item['Geometry']['BoundingBox']['Height'] * 250,
        #                 item['Geometry']['BoundingBox']['Left'] * 100,
        #                 item['Geometry']['BoundingBox']['Top'] * 150,
        #             ])
        #     arrayzao[val] = geral
        #     geral = []

        # return TratamentoOCR(arrayzao).format()
