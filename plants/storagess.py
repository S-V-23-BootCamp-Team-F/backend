import boto3
import uuid
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file):
        return self.client.upload(file)

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        print(secret_key)
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key
        )
        self.s3_client   = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try:
            print(str(file))
            file_id    = 'images/'+str(uuid.uuid4())+'.png'
            file_name = str(uuid.uuid4())+'.png'
            extra_args = { 'ContentType' : file.content_type }
            print(extra_args)
            
            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    file_id,
                    ExtraArgs = extra_args
                )
            #return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
            return f'{file_name}'
        except :
            return None

# MyS3Client instance
s3_client = MyS3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY,S3_BUCKET_NAME)