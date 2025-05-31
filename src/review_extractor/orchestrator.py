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

    def __init__(self, api_key: str, google_api_key: str):
        self.api_key = api_key
        self.google_api_key = google_api_key

    def start(self, text: str) -> dict:
        logger.info("start")
        client = OpenAI(api_key=self.api_key)
        extracted = self.extract_user_interest(text, client)
        user_query = extracted["query"]
        demographics = extracted["demographics"]

        places = self.search_places_by_text(user_query, location_bias="New York City")
        logger.info(f"Places found: {places}")
        revs = []
        for place in places:
            logger.info(f"Place: {place['name']}, Address: {place['address']}, Rating: {place['rating']}")
            reviews = self.get_place_details_with_reviews(place['place_id'])
            revs.append({
                "name": place['name'],
                "rating": place['rating'],
                "address": place['address'],
                "reviews": reviews
            })
            logger.info(f"Reviews for {place['name']}: {len(reviews)} reviews")

        return {"user_query": user_query, "demographics": demographics, "places": revs}

    def extract_user_interest(self, text: str, client: OpenAI) -> dict:
        instructions = """
        You are a helpful assistant. A user will provide a piece of text containing:
        - Their interests or place they're inquiring about
        - Personal or demographic data (age, gender, location, etc.)
        - Additional details or preferences

        Your job is to extract:
        1. The user's query (for searching places)
        2. Any available demographic or personalization data

        Return a JSON object like:
        {
            "query": "best sushi in Brooklyn",
            "demographics": {
                "age": "30",
                "location": "Brooklyn",
                "gender": "female",
                "language": "English",
                "dialect": "African American Vernacular English"
            }
        }
        """

        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ]

        response = client.chat.completions.create(
            model='gpt-4.1-mini-2025-04-14',
            messages=messages
        )

        return json.loads(response.choices[0].message.content)

    def search_places_by_text(self, query: str, location_bias: str = "New York City") -> list:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": query,
            "key": self.google_api_key,
        }
        if location_bias:
            params["location"] = location_bias
            params["radius"] = 5000

        response = requests.get(url, params=params)
        results = response.json().get("results", [])

        if not results:
            logger.warning("No matching places found.")
            return []

        places = []
        for place in results[:5]:
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
            "fields": "name,rating,user_ratings_total,reviews",
            "key": self.google_api_key,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "OK":
            logger.warning(f"Google API Error: {data.get('status')}")
            return []

        raw_reviews = data["result"].get("reviews", [])

        reviews = [
            {
                "author_name": r.get("author_name"),
                "rating": r.get("rating"),
                "text": r.get("text"),
                "time": r.get("time"),
                "relative_time_description": r.get("relative_time_description")
            }
            for r in raw_reviews
        ]
        return reviews
