class FormatData:

    def __init__(self, object_name):
        self.object_name = object_name
        self.result_values = {}

    def result_search(self, value: list):
        out_values = []
        for i in range(len(value[1])):
            out_values.append({
                'Quantity': value[0][i].strip(),
                'Material': value[1][i].strip(),
                'Unit_price': value[2][i].strip()
            })
        self.result_values[self.object_name] = out_values

    def get_result_search(self):
        return self.result_values
