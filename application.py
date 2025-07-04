from src.review_extractor.main import handler

if __name__ == "__main__":
    event = {
        "Records": [
                {
                    "eventVersion": "2.1",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "2025-07-03T00:32:43.887Z",
                    "eventName": "ObjectCreated:CompleteMultipartUpload",
                    "userIdentity": {
                        "principalId": "A3I02SFF08H2BT"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "69.116.139.232"
                    },
                    "responseElements": {
                        "x-amz-request-id": "WKQ7TEW8PV1DG66J",
                        "x-amz-id-2": "Kcx0KbQyUeemqdo2Eiyr1/8oxYmYUv3vgatB6b+LptJ17y5/yEM9+5O8pGB47jYjg9lWjReN4fvIcWwLM/e/UEjmi5vqtmO7"
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "291585cc-e910-45ae-99b9-f6e6f89ccb23",
                        "bucket": {
                            "name": "vidx-clip-videos",
                            "ownerIdentity": {
                                "principalId": "A3I02SFF08H2BT"
                            },
                            "arn": "arn:aws:s3:::vidx-clip-videos"
                        },
                        "object": {
                            "key": "1087722138833780807/2025-07-04/1390723139604058162_1v1.mp4",
                            "size": 80426152,
                            "eTag": "74b76461812fbd8046a878befc52ed80-5",
                            "sequencer": "006865CFA427DFE4C2"
                        }
                    }
                }
            ]
        }
    

    handler(event, {})
    
    prompts = [
        {            "prompt_name": "transcribe audio",
            "prompt_content": "Can you transcribe the audio on this video and give me all the audio output in text"
        },
        {            "prompt_name": "sentiment_analysis",
            "prompt_content": "Task: You are an expert at analyzing video and audio to extract moments of excitement and sentiment. Given an audio or video segment, carefully review the audio to detect signs of excitement or high-intensity moments. Consider as excitement: -Shouting -Laughing -Cheering -Crowd noise -Celebration sounds (e.g., applause, goal, win, victory sounds) -Sudden increase in loudness or pitch If you find any excitement or intense moment, identify the exact timestamp (in seconds or mm:ss) where it occurs, and explain the reason for your judgment. If there is no excitement present, return 'neutral' as sentiment, and explain briefly. Your response must be a JSON object with these fields: sentiment: 'excited' or 'neutral' reason: Short explanation of your judgment (e.g., 'cheering and laughter detected at 01:23') timestamp: Timestamp of excitement (if any), or null if neutral"
        },
        {            "prompt_name": "metadata",
            "prompt_content": "summarize the video, generate hashtags, and find the category of the video. Categories are: 1 **world pvp** - Usually out in the open field where there are between 2-20 allies engaging in combat with enemies. 2 **OPR** - Instance player vs player where a team of exactly 5 fights against other groups of players. 3 **Arena** - team of 3 allies fighting against a team of 3 enemies in a closed arena. 4 **Clutch pvp** - One player by himself is able to fight and defeat multiple opponents. The output should be a json object containing **description**, **category**, **hashtags**"
        },
        {            "prompt_name": "video_highlights",
            "prompt_content": "What are the highlights of this video? What are the most important moments?"
        }
    ]
