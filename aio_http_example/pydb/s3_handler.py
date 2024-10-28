import boto3
from botocore.exceptions import ClientError
import tempfile
from pydb.logger import logger


class S3Client:
    """
    A wrapper class for AWS S3 operations using boto3.
    Provides methods for common S3 operations such as uploading,
    downloading, listing objects, and generating presigned URLs.
    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='us-west-2'):
        """
        Initializes the S3 client with a specified region.

        :param aws_access_key_id: AWS access key.
        :param aws_secret_access_key: AWS secret access key.
        :param region_name: AWS region where the S3 bucket is located. Default is 'us-west-2'.
        """
        self.s3_client = boto3.client('s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self._object = None 

    def init_object(self, _object):
        """
        Initialize the Pydantic object to be used for operations.

        :param _object: Pydantic object containing the data for upload.
        """
        self._object = _object

    def upload_file_from_temp(self, bucket_name, key):
        """
        Saves the Pydantic object's model_dump() output into a temporary file 
        and uploads it to the specified S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param key: The key (name) for the uploaded object in S3.
        :return: None
        """
        if not self._object:
            logger.error("Pydantic object is not initialized. Use init_object() to set it.")
            return

        content = self._object.model_dump_json()

        try:
            with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
                tmp_file.write(content.encode())
                tmp_file.flush()
                
                self.s3_client.upload_file(tmp_file.name, bucket_name, key)
                logger.info(f"File uploaded to S3: {bucket_name}/{key}")

        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while handling tempfile: {e}")

    def download_file(self, bucket_name, key, file_name):
        """
        Downloads a file from the specified S3 bucket and saves it to the local file system.

        :param bucket_name: Name of the S3 bucket.
        :param key: The key (name) of the object in S3.
        :param file_name: The local path where the file will be saved.
        :return: None
        """
        try:
            self.s3_client.download_file(bucket_name, key, file_name)
            logger.info(f"File downloaded from S3: {file_name}")
        except ClientError as e:
            logger.error(f"Error downloading from S3: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during file download: {e}")

    def generate_presigned_url(self, bucket_name, key, expiration=3600):
        """
        Generates a presigned URL to share an S3 object.

        :param bucket_name: Name of the S3 bucket.
        :param key: The key (name) of the object in S3.
        :param expiration: Time in seconds for the presigned URL to remain valid. Default is 3600 seconds (1 hour).
        :return: The presigned URL as a string, or None if an error occurs.
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': key
                    },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def list_objects(self, bucket_name, prefix=""):
        """
        Lists objects in the specified S3 bucket, optionally filtered by a prefix.

        :param bucket_name: Name of the S3 bucket.
        :param prefix: Filter objects by this prefix. Defaults to an empty string (no filter).
        :return: A list of object keys, or None if an error occurs.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            else:
                logger.info(f"No objects found in {bucket_name} with prefix '{prefix}'")
                return []
        except ClientError as e:
            logger.error(f"Error listing objects in bucket: {e}")
            return None

    def delete_object(self, bucket_name, key):
        """
        Deletes an object from the specified S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param key: The key (name) of the object in S3.
        :return: None
        """
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=key)
            logger.info(f"Object {key} deleted from {bucket_name}")
        except ClientError as e:
            logger.error(f"Error deleting object from S3: {e}")
