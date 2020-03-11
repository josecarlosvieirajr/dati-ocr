from services.ocr.ocr_connect import ConnectOcr


class GeneralOCR(ConnectOcr):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.data = None
        self.file = None

    def run(self, file):
        self.file = file
        if self.ocr_di_data():
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


    def general_ocr(self):
        size = 100
        pag = 0
        front_table = []
        render_front = {}
        if self.data['DocumentMetadata']['Pages'] > 1:
            for item in self.data['Blocks']:
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
            for item in self.data['Blocks']:
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
