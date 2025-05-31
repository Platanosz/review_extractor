import os
from .orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['API_KEY']

orchestrator = Orchestrator(api_key)