from datetime import datetime
from dotenv import load_dotenv
import boto3
import time
import re

load_dotenv()


class ConnectionOCR:
    RESPONSE: str

    def __init__(self, s3_bucket_name, object_name):
        self.s3_bucket_name = s3_bucket_name
        self.object_name = object_name
        self.client = boto3.client('textract')

    def start_job(self):

        response = self.client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': self.s3_bucket_name,
                    'Name': self.object_name
                }
            },
            FeatureTypes=['FORMS']
        )

        self.RESPONSE = response["JobId"]

    def is_job_complete(self):
        response = self.client.get_document_analysis(JobId=self.RESPONSE)
        status = response["JobStatus"]

        while status == "IN_PROGRESS":
            response = self.client.get_document_analysis(JobId=self.RESPONSE)
            status = response["JobStatus"]

        return status

    def get_job_results(self):
        return self.client.get_document_analysis(JobId=self.RESPONSE)

        # pages.append(response)
        # next_token = None
        # if 'NextToken' in response:
        #     next_token = response['NextToken']
        #
        # while next_token:
        #     response = client.get_document_text_detection(JobId=self.RESPONSE, NextToken=next_token)
        #
        #     pages.append(response)
        #     next_token = None
        #     if 'NextToken' in response:
        #         next_token = response['NextToken']
        #
        # return pages

    @staticmethod
    def get_comprehend(text):
        comprehend = boto3.client('comprehendmedical')
        return comprehend.detect_entities(Text=text)
