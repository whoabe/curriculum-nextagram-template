import boto3, botocore
from config import Config
from flask_login import current_user
import braintree
# S3_KEY, S3_SECRET, S3_BUCKET

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=Config.MERCHANT_ID,
        public_key=Config.PUBLIC_KEY,
        private_key=Config.PRIVATE_KEY
    )
)

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            str(current_user.id)+"-"+file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}-{}".format(Config.S3_LOCATION, str(current_user.id), file.filename)


# http://next-curriculum-instagram.s3.amazonaws.com/testtest2-boo.png
# adds username - boo.png

# http://abe-next-clone-instagram.s3.amazonaws.com/up.png
# S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)