import boto3

# Document
s3BucketName = "ocrdatidev"
documentName = "IE_OOO.pdf"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    })

print(response)
#
# for page in response.pages:
#     # Print fields
#     print("Fields:")
#     for field in page.form.fields:
#         print("Key: {}, Value: {}".format(field.key, field.value))
#
#     # Get field by key
#     print("\nGet Field by Key:")
#     key = "Phone Number:"
#     field = page.form.getFieldByKey(key)
#     if field:
#         print("Key: {}, Value: {}".format(field.key, field.value))
#
#     # Search fields by key
#     print("\nSearch Fields:")
#     key = "address"
#     fields = page.form.searchFieldsByKey(key)
#     for field in fields:
#         print("Key: {}, Value: {}".format(field.key, field.value))
