from review_extractor import orchestrator
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Received event: {event}")
    message = orchestrator.start(event['text'])
    logger.info(f"Processed message: {message}")
    return {
        "statusCode": 200,
        "messages_processed": message

    }
    
