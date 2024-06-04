# Upload to GCS
from google.cloud import storage
import os

def upload_to_gcs(bucket_name, source_folder, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            #if '.keras' in file:
                local_path = os.path.join(root, file)
                blob_path = os.path.relpath(local_path, source_folder)
                blob = bucket.blob(os.path.join(destination_blob_name, blob_path))
                blob.upload_from_filename(local_path)
                print(f"Uploaded {local_path} to {blob_path}")

bucket_name = 'reddit_raw_data_0184598608709384596'
source_folder = 'tf_model_v2'
destination_blob_name = 'model_v2/'
print('start upload')

upload_to_gcs(bucket_name, source_folder, destination_blob_name)