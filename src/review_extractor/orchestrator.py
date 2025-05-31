from botocore.exceptions import ClientError
import json
from openai import OpenAI
import boto3
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(asctime)s [%(filename)s:%(lineno)d]: %(message)s'
                    )
logger = logging.getLogger(__name__)


class Orchestrator:

    def __init__(self, api_key:str):
        self.api_key = api_key    
        
    def start(self, text: str) -> str:
        logger.info(f"start")
        client = OpenAI(api_key=self.api_key)
        automated_message = self.extract_user_interest(text, client)
        return automated_message
    
    def extract_user_interest(self, text: str, client: OpenAI):
    
        instructions = f"""
        You are a helpful assistant that extracts user interests from a given text."""
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ]
        response = client.chat.completions.create(
            model='gpt-4.1-mini-2025-04-14',
            messages=messages
        )
        return response.choices[0].message.content      
    
