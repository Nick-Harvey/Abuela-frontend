import os
import logging
from google.cloud import storage
from decouple import config

#PROJECT = config('GCLOUD_PROJECT')
CREDS = config('GOOGLE_APPLICATION_CREDENTIALS')

client = storage.Client()

class objectStore():

	def upload_blob(bucket_name, uploaded_file, destination_blob_name):
		"""Uploads a file to the GCS bucket."""
		#TODO Add something to check if the file has already be added in the last 60 seconds

		#client = storage.Client()
		bucket = client.get_bucket('abuela_input_images_dev')
		blob = bucket.blob(destination_blob_name)

		blob.upload_from_file(uploaded_file, rewind=True)
		logging.info(
			"File {} uploaded to {}.".format(
				uploaded_file.name, destination_blob_name
				)
			)

	def download_blob(bucket_name):
	    """Downloads a blob from the bucket."""
	    # dev bucket_name = "abuela_output_images_dev"
	    # destination_file_name = "local/path/to/file"

	    for blob in client.list_blobs(bucket_name, prefix='/final_output/'):
	    	filename = blob.name
	    	restored_image = blob.download_as_bytes()
	
	    print(
	        "Blob {} downloaded to localhost.".format(filename)
	    )
	    return restored_image
