from src.review_extractor.main import handler

if __name__ == "__main__":
    event = {
        "body": '{\n        "text": "italian restaurant near Empire State Building"\n        }'
        }

    handler(event, {})
