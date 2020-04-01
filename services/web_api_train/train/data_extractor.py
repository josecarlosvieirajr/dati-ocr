import json
import pandas as pd
import redis
import regex
from typing import NoReturn, List

from services.web_api_train.train.services.find_items_in_ocr import FindItemsOcr
from validators.values_select_by_regex import ValidateSelectByRegex

db = redis.Redis()


class DataExtractor:
    def __init__(self, data: dict):
        self.data = data
        self.name = f'base_{data["name"]}'
        self.part_numbers = data['part_numbers']
        self.quantities = data['quantities']
        self.unit_prices = data['unit_prices']
        self.switch = False
        self.data_from_doc = list()

    def run(self):
        item_ocr = FindItemsOcr(self.data)
        self.data_from_doc = item_ocr.do_your_magic()

        if not self.data_from_doc:
            self.backup_plan_b()

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
            part_numbers_regx.append(self.create_all_regx(part))
            quantities_regx.append(self.create_all_regx(qtd))
            unit_prices_regx.append(self.create_all_regx(unit))

        return part_numbers_regx, quantities_regx, unit_prices_regx

    @staticmethod
    def create_all_regx(all_value):
        value_regx = []
        for value in all_value:
            for digit in value:
                regx = None
                if digit.isnumeric():
                    regx = '[0-9]'
                if digit.isalpha():
                    regx = '[a-zA-Z]'
                if not digit.isalnum():
                    regx = f"*\{digit}"
                value_regx.append(regx)

        value_regx = ValidateSelectByRegex(value_regx).validate_value_regx()
        return value_regx

    def identify_standards_words(self, regx_compile):
        if self.switch:
            return self.two_way_of_doing_things(regx_compile)
        return self.one_way_of_doing_things(regx_compile)

    def one_way_of_doing_things(self, regx_compile):
        words_find = []
        for key in self.data_from_doc:
            for data in self.data_from_doc[key]:
                for i in data.split():
                    if regex.findall(regx_compile, i.strip()):
                        words_find.append(i.strip())

        return words_find

    def two_way_of_doing_things(self, regx_compile):
        words_find = []
        for data in self.data_from_doc:
            for i in data.split():
                if regex.findall(regx_compile, i.strip()):
                    words_find.append(i.strip())

        return words_find

    @staticmethod
    def format_data(v):
        top = []
        flatten = lambda l: [item for sublist in l for item in sublist]

        for i in v:
            result = list(i.values())
            for a in result:
                top.append(list(a.values()))

        return flatten(top)

    def backup_plan_b(self):
        self.switch = True
        self.data_from_doc = self.format_data(json.loads(db.get(self.name).decode("UTF-8"))["obj"])
