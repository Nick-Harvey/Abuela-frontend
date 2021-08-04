import logging
from google.cloud import storage
from decouple import config

# PROJECT = config('GCLOUD_PROJECT')
CREDS = config('GOOGLE_APPLICATION_CREDENTIALS')


class ObjectStore:
    def __init__(self):
        self.client = storage.Client()

    def upload_blob(self, bucket_name, uploaded_file, destination_blob_name):
        """Uploads a file to the GCS bucket."""
        # TODO Add something to check if the file has already be added in the last 60 
        # seconds

        # client = storage.Client()
        bucket = self.client.get_bucket('abuela_input_images_dev')
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_file(uploaded_file, rewind=True)
        logging.info(
            "File {} uploaded to {}.".format(
                uploaded_file.name, destination_blob_name
                )
            )

    def download_blob(self, bucket_name, file):
        """Downloads a blob from the bucket."""
        # dev_bucket_name = "abuela_output_images_dev"
        # destination_file_name = "local/path/to/file"

        for blob in self.client.list_blobs(bucket_name, prefix='/final_output/'):
            filename = blob.name
            
            try:
                restored_image = blob.download_as_bytes(file.name)

                logging.info(
                    "File {} downloaded to localhost.".format(filename)
                )

            except Exception as e:
                logging.error("unable to download file: {}".format(e))
    
            return restored_image
