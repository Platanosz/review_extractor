import os
from .orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['API_KEY']
google_api_key = os.environ['GOOGLE_API_KEY']

orchestrator = Orchestrator(api_key, google_api_key)