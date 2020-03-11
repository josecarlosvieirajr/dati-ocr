# import boto3
#
#
# class TratamentoOCR:
#     def __init__(self, obj):
#         self.obj = obj
#
#     def format(self):
#
#         comprehend = boto3.client('comprehendmedical')
#
#         ids_list = []
#         big = 0
#         for i in self.obj['Blocks']:
#             try:
#                 for a in i['Relationships']:
#                     if len(a['Ids']) > big:
#                         big = len(a['Ids'])
#                     if len(a['Ids']) >= big:
#                         ids_list.append(a['Ids'])
#             except Exception:
#                 continue
#
#         geral = []
#         for item in self.obj['Blocks']:
#             for id_item in ids_list[0]:
#                 if id_item is item['Id']:
#                     if item["BlockType"] == "LINE":
#                         geral.append([
#                             item['Text'],
#                             item['Geometry']['BoundingBox']['Width'] * 100,
#                             item['Geometry']['BoundingBox']['Height'] * 250,
#                             item['Geometry']['BoundingBox']['Left'] * 100,
#                             item['Geometry']['BoundingBox']['Top'] * 230,
#                         ])
#
#         total = []
#         for text in geral:
#             total.append(comprehend.detect_entities(Text=text[0]))
#
#         # total = EnumTeste.COMPREHEND.value
#         # geral = EnumTeste.FRONT_TEST.value
#
#         total_comprehend = []
#         for i in total:
#             for a in i['Entities']:
#                 if 'ID' not in a['Type']:
#                     total_comprehend.append(a['Text'])
#         geral_label = []
#         for i in geral:
#             geral_label.append(i[0])
#
#         result_label = []
#         for i in total_comprehend:
#             for a in geral_label:
#                 if a not in i and a not in result_label:
#                     result_label.append(a)
#         top = []
#         for i in result_label:
#             if '/' not in i and '@' not in i and 4 < len(i) < 10 and '<' not in i:
#                 top.append(i)
#         geral_finalisou = []
#         for t in top:
#             for i in geral:
#                 if t == i[0]:
#                     geral_finalisou.append(i)
#
#         return geral_finalisou
