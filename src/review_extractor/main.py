from review_extractor import orchestrator
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Received event: {event}")
    body = json.loads(event['body'])
    text = body.get("text")
    message = orchestrator.start(text)
    logger.info(f"Processed message: {message}")
    return {
        "statusCode": 200,
        "body": message

    }
    
