import pandas as pd


class FindItemsOcr:
    def __init__(self, data):
        self.data: dict = data
        self.df: pd.DataFrame = pd.read_pickle(f"./dummy_{self.data['name']}.pkl")

    def do_your_magic(self):
        result = {}
        flatten = lambda l: [item for sublist in l for item in sublist]
        union_data = flatten(flatten([self.data["part_numbers"], self.data["quantities"], self.data["unit_prices"]]))
        req_obj = self.where_are_the_requested_objects(union_data)
        if not req_obj:
            return []
        for obj in req_obj:
            result[obj[3]] = self.df[obj[3]].to_numpy()
        return result

    def where_are_the_requested_objects(self, union_data):
        result = []
        rows = self.df.shape[0] + 1
        columns = self.df.shape[1] + 1
        for row in range(1, rows):
            for column in range(1, columns):
                for i in union_data:
                    aux = str(self.df._get_value(row, column)).find(i)
                    if aux != -1:
                        result.append([i, aux, row, column])
        return result