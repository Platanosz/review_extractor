from review_extractor import orchestrator
import logging
import json
import boto3
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


s3 = boto3.client('s3')

def handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    records = event.get('Records', [])
    for record in records:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        logger.info(f"Processing file from bucket: {bucket}, key: {key}")

        # 2. Download file to /tmp
        file_name = key.split('/')[-1]
        local_path = f'/tmp/{file_name}'
        s3.download_file(bucket, key, local_path)
        logger.info(f"Downloaded {key} to {local_path}")

        # 3. Process the file (your logic here)
        # Example: Just print size, but here you could use ffmpeg, analyze, etc.
        with open(local_path, 'rb') as f:
            files = {'file': (file_name, f)}
            # response = requests.post(
            #     "https://api.example.com/upload",  # <-- Your external API endpoint
            #     files=files,
            #     headers={"Authorization": "Bearer <your_token>"}  # Add any required headers
            # )
            logger.info(f"External API response: {file_name} processed successfully")

        # Optionally: clean up file
        os.remove(local_path)

        # Example: (Optionally, save or upload results)
        # processed_file = process_video(local_path)
        # s3.upload_file(processed_file, bucket, f'processed/{file_name}')

    return {
        'statusCode': 200,
        'body': 'Processing complete'
    }
    
