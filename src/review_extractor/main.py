from review_extractor import orchestrator
import logging
import json
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    records = event.get('Records', [])
    for record in records:
        orchestrator.start(record)

        # Example: (Optionally, save or upload results)
        # processed_file = process_video(local_path)
        # s3.upload_file(processed_file, bucket, f'processed/{file_name}')

    return {
        'statusCode': 200,
        'body': 'Processing complete',
        "keys": [record.get('s3', {}).get('object', {}).get('key', '') for record in records]
    }
    
