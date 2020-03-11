import boto3
from dotenv import load_dotenv

# from datiocr.service.task import DatiOcr

load_dotenv()


class GeneralOCR:

    def run(self, bucket, doc):
        size = 100
        pag = 0
        front_table = []
        render_front = {}
        status = "IN_PROGRESS"
        response_status = dict()
        client = boto3.client('textract')
        comprehend = boto3.client('comprehendmedical')

        response = client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': doc
                }
            },
            FeatureTypes=['TABLES']
        )

        while status == "IN_PROGRESS":
            response_status = client.get_document_analysis(JobId=response["JobId"])
            status = response_status["JobStatus"]
        print('Total de Paginas', response_status['DocumentMetadata']['Pages'])
        if response_status['DocumentMetadata']['Pages'] > 1:
            for item in response_status['Blocks']:
                if item["BlockType"] == "LINE":

                    if item['Page'] > pag:
                        print('PAGINA ', pag+1, item['Text'])
                        render_front[pag+1] = front_table
                        front_table = []
                    pag = item['Page']
                    # multiply = item['Page'] if item['Page'] == 1 else item['Page'] * 2.3
                    front_table.append([
                        item['Text'],
                        item['Geometry']['BoundingBox']['Width'] * size,
                        item['Geometry']['BoundingBox']['Height'] * size * 2.5,
                        item['Geometry']['BoundingBox']['Left'] * size,
                        item['Geometry']['BoundingBox']['Top'] * size * 2.3 * (item['Page'] * 3),
                    ])
        else:
            for item in response_status['Blocks']:
                if item["BlockType"] == "LINE":
                    front_table.append([
                        item['Text'],
                        item['Geometry']['BoundingBox']['Width'] * size,
                        item['Geometry']['BoundingBox']['Height'] * size * 2.5,
                        item['Geometry']['BoundingBox']['Left'] * size,
                        item['Geometry']['BoundingBox']['Top'] * size * 2.3,
                    ])
            render_front['1'] = front_table

        return render_front
        # for table in front_table:
        #     front_table_intelligent.append(comprehend.detect_entities(Text=table[0]))
        #
        # for item in front_table_intelligent:
        #     for a in item['Entities']:
        #         if a['Type'] == 'ID':
        #             render_front.append(a['Text'])
        #     for b in item['UnmappedAttributes']:
        #         render_front.append(b['Attribute']['Text'])
        #
        # values = []
        #
        # for i in front_table:
        #     for a in render_front:
        #         if i[0] == a:
        #             values.append(i)
        #
        # add = []
        # for i in range(len(values)):
        #     try:
        #         if values[i] != values[i + 1]:
        #             add.append(values[i])
        #     except Exception:
        #         break
        # return add
