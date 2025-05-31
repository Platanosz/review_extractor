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

    def __init__(self, api_key:str, google_api_key:str):
        self.api_key = api_key    
        self.google_api_key = google_api_key
        
    def start(self, text: str) -> str:
        logger.info(f"start")
        client = OpenAI(api_key=self.api_key)
        user_query = self.extract_user_interest(text, client)
        places = self.search_places_by_text(user_query, location_bias="New York City")
        logger.info(f"Places found: {places}")
        revs = []
        for place in places:
            logger.info(f"Place: {place['name']}, Address: {place['address']}, Rating: {place['rating']}")
            reviews = self.get_place_details_with_reviews(place['place_id'])
            revs.append(reviews)
            logger.info(f"Reviews for {place['name']}: {reviews.get('user_ratings_total', 0)} ratings, Average rating: {reviews.get('rating', 'N/A')}, {reviews.get('reviews', [])}") 
        return {"user_query": user_query, "reviews": revs}
    
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

    def search_places_by_text(self, query: str, location_bias: str="New York City") -> list:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": query,
            "key": self.google_api_key,
        }
        if location_bias:
            params["location"] = location_bias
            params["radius"] = 5000  # meters

        response = requests.get(url, params=params)
        results = response.json().get("results", [])
        
        if not results:
            print("No matching places found.")
            return []

        places = []
        for place in results[:5]:  # Limit to top 5 results
            places.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "place_id": place.get("place_id"),
            })

        return places
    
    def get_place_details_with_reviews(self, place_id):
        url = f"https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,rating,review,user_ratings_total",
            "key": self.google_api_key,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") == "OK":
            return data["result"]
        else:
            print(f"Error: {data.get('status')}")
    
