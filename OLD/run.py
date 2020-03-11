from OLD.datiocr import EnumTeste

front_table = {}
add = []
size = 100
pag = 0
response_status = EnumTeste.BACK_TEST.value
if response_status['DocumentMetadata']['Pages'] > 1:
    for item in response_status['Blocks']:
        if item["BlockType"] == "LINE":
            if item['Page'] != pag and pag != 0:
                front_table[pag] = add
                add = []

            if item['Page'] > pag:
                pag = item['Page']

    print(front_table[2])
