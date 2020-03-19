import ast
import re
from typing import NoReturn, List

import redis

db = redis.Redis()


class DataExtractor:
    def __init__(self, data: dict):
        self.part_numbers = data['part_numbers']
        self.quantities = data['quantities']
        self.unit_prices = data['unit_prices']
        self.data_from_doc = list()

    def run(self):

        data_from_redis = db.lrange('base', 0, db.llen('base'))
        for data in data_from_redis:
            self.data_from_doc.append(data.decode("UTF-8"))
        part_numbers_regx, quantities_regx, unit_prices_regx = self.create_regex()

        part_numbers_result, quantities_result, unit_prices_result = [], [], []

        for part, qtd, unit in zip(part_numbers_regx, quantities_regx, unit_prices_regx):
            part_numbers_result.append(self.identify_standards_words(part))
            quantities_result.append(self.identify_standards_words(qtd))
            unit_prices_result.append(self.identify_standards_words(unit))

        return [part_numbers_result, quantities_result, unit_prices_result]

    def create_regex(self):
        part_numbers_regx, quantities_regx, unit_prices_regx = [], [], []
        for part, qtd, unit in zip(self.part_numbers, self.quantities, self.unit_prices):
            part_numbers_regx.append(re.compile(self.create_all_regx(part)))
            quantities_regx.append(re.compile(self.create_all_regx(qtd)))
            unit_prices_regx.append(re.compile(self.create_all_regx(unit)))

        return part_numbers_regx, quantities_regx, unit_prices_regx

    @staticmethod
    def create_all_regx(all_value):
        value_regx = str()
        for value in all_value:
            for digit in value:
                regx = None
                if digit.isnumeric():
                    regx = '[0-9]'
                if digit.isalpha():
                    regx = '[a-zA-Z]'
                if not digit.isalnum():
                    regx = f"*\{digit}"
                value_regx = value_regx + regx

        return value_regx

    def identify_standards_words(self, regx_compile):
        words_find = []
        for words in self.data_from_doc:
            if re.match(regx_compile, words):
                words_find.append(words)
        return words_find
