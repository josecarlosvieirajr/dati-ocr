class ValidateSelectByRegex:
    def __init__(self, params):
        self.params = params

    def validate_value_regx(self):

        ttp = self.identify_unique_type()

        return self.format_init_and_finish_regx(ttp)

    def identify_unique_type(self):
        if self.check_equal(self.params):
            return len(self.params)
        return 0

    @staticmethod
    def check_equal(iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    def format_string(self):
        aux = str()
        for i in self.params:
            aux = aux + i
        return aux

    def format_init_and_finish_regx(self, ttp):
        if ttp != 0:
            qtd_str = "{%s}" % ttp
            return f"^{self.params[0]}{qtd_str}$"
        else:
            return f"^{self.format_string()}$"
