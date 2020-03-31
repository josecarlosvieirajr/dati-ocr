class FindTableOCR:
    def __init__(self, data_doc):
        self.data_doc = data_doc

    def run(self):
        return self.generate_table()

    def get_rows_columns_map(self, table_result, blocks_map):
        rows = {}
        for relationship in table_result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            rows[row_index] = {}
                        rows[row_index][col_index] = self.get_text(cell, blocks_map)
        return rows

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

    def generate_table(self):
        blocks = self.data_doc["Blocks"]
        blocks_map_out = {}
        table_blocks = []
        for block in blocks:
            blocks_map_out[block['Id']] = block
            if block['BlockType'] == "TABLE":
                table_blocks.append(block)
        valid_csv = []
        for index, table in enumerate(table_blocks):
            valid_csv.append(self.get_rows_columns_map(table, blocks_map_out))
        return valid_csv
