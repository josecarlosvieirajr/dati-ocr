from datetime import datetime

import boto3
import time
import re


class ConnectionOCR:
    RESPONSE: str

    def __init__(self, s3_bucket_name, object_name):
        self.s3_bucket_name = s3_bucket_name
        self.object_name = object_name

    def start_job(self):
        client = boto3.client('textract')
        response = client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': self.s3_bucket_name,
                    'Name': self.object_name
                }
            })

        self.RESPONSE = response["JobId"]

    def is_job_complete(self):
        time.sleep(5)
        client = boto3.client('textract')
        response = client.get_document_text_detection(JobId=self.RESPONSE)
        status = response["JobStatus"]

        while status == "IN_PROGRESS":
            time.sleep(15)
            response = client.get_document_text_detection(JobId=self.RESPONSE)
            status = response["JobStatus"]

        return status

    def get_job_results(self):
        pages = []
        time.sleep(5)

        client = boto3.client('textract')
        response = client.get_document_text_detection(JobId=self.RESPONSE)

        pages.append(response)
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']

        while next_token:
            time.sleep(5)

            response = client.get_document_text_detection(JobId=self.RESPONSE, NextToken=next_token)

            pages.append(response)
            next_token = None
            if 'NextToken' in response:
                next_token = response['NextToken']

        return pages

    @staticmethod
    def get_comprehend(text):
        comprehend = boto3.client('comprehendmedical')
        return comprehend.detect_entities(Text=text)
