import pandas as pd


class FindTableOCR2:
    def __init__(self, data_doc):
        self.data_doc = data_doc

    def run(self):
        return self.get_table_csv_results(self.data_doc)

    def get_table_csv_results(self, response):

        blocks = response['Blocks']

        blocks_map = {}
        table_blocks = []
        for block in blocks:
            blocks_map[block['Id']] = block
            if block['BlockType'] == "TABLE":
                table_blocks.append(block)

        if len(table_blocks) <= 0:
            return "<b> NO Table FOUND </b>"

        csv = ''
        for index, table in enumerate(table_blocks):
            csv += self.get_rows_columns_map(table, blocks_map)
        return csv

    def get_rows_columns_map(self, table_result, blocks_map):
        rows = {}
        df = pd.DataFrame()
        for relationship in table_result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}
                        df._set_value(row_index, col_index,  self.get_text(cell, blocks_map))

        return df

    @staticmethod
    def get_text(result, blocks_map):
        text = ''
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] == 'SELECTED':
                                text += 'X '
        return text
