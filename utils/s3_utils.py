import boto3
import uuid
import os

from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"
S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file, folder="shop_owners"):
    file_extension = file.filename.split(".")[-1]
    file_key = f"{folder}/{uuid.uuid4()}.{file_extension}"
    s3_client.upload_fileobj(
        file.file,
        S3_BUCKET_NAME,
        file_key,
        ExtraArgs={"ACL": "public-read", "ContentType": file.content_type}
    )
    s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
    return s3_url
