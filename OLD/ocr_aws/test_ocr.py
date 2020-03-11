import random
from datetime import datetime

import boto3
import time
import re

init = datetime.now()


def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        })

    return response["JobId"]


def isJobComplete(jobId):
    time.sleep(5)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    # print("Job status: {}".format(status))

    while (status == "IN_PROGRESS"):
        time.sleep(15)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        # print("Job status: {}".format(status))

    return status


def getJobResults(jobId):
    pages = []

    time.sleep(5)

    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)

    pages.append(response)
    nextToken = None
    if 'NextToken' in response:
        nextToken = response['NextToken']

    while (nextToken):
        time.sleep(5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        nextToken = None
        if 'NextToken' in response:
            nextToken = response['NextToken']

    return pages


# Document
s3BucketName = "ocrdatidev"
documentName = 'AI_000.pdf'
# documentName = pdf_values

jobId = startJob(s3BucketName, documentName)
response = ''
if isJobComplete(jobId):
    response = getJobResults(jobId)
text = ''

for resultPage in response:
    print(resultPage)
    print('########################################################################')
    for item in resultPage["Blocks"]:
        print(item)
#         if item["BlockType"] == "LINE":
#             text = text + " " + item["Text"]
#
# # print(text)
#
# quantity = re.findall('\s[1-9][0-9]{0,3}[A-Za-z]{3}', text)
# material = re.search('\s[a-zA-Z]{1,4}[+]\S', text)
# unit_price = re.findall('\s[$][1-9][0-9]{0,3}[.][0-9]{2}\s', text)
#
# entity_types = []
# comprehend = boto3.client('comprehendmedical')
# entities = comprehend.detect_entities(Text=text)
#
# print(quantity, material.groups(), unit_price)
#
# for q in quantity:
#     for entity in entities["Entities"]:
#         print(entity['Text'])

# def result_search(value: list):
#     out_values = []
#     for i in range(len(value[1])):
#         out_values.append({
#             'Quantity': value[0][i].strip(),
#             'Material': value[1][i].strip(),
#             'Unit_price': value[2][i].strip()
#         })
#     list_result_values[pdf_values] = out_values
#
#
# if len(material) == 1:
#     result_search([quantity, material, unit_price])
#
# else:
#     for q in quantity:
#         [quantity.remove(q) for entity in entities["Entities"] if q.strip() in entity['Text']]
#     result_search([quantity, material, unit_price])
#
# print(list_result_values)
# print(f"###### TIME EXECUTION FOR {len(lista)}-PDFS IS: {datetime.now() - init} ######")
