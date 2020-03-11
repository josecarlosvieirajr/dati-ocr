import re

from OLD.datiocr import EnumTeste

ALL_DATA = EnumTeste.FRONT_TEST.value
DATA_SEND_FRONT = ['100062658', '17.280,00', '1,72000']
regex = ''
if DATA_SEND_FRONT[0].isnumeric():
    regex += '\d{%s}' % len(DATA_SEND_FRONT[0])

    for send in DATA_SEND_FRONT[0]:
        regex = '[%s][0-9]{%s}' % (send, (len(DATA_SEND_FRONT[0]) - 1))
        break

regex = re.compile(regex)
abc = []
for all_t in ALL_DATA:
    try:
        if re.match(regex, all_t[0]).group():
            abc.append(all_t[0])
    except Exception as e:
        print(e)

for i in abc:
    if abc != '':
        print(abc)
