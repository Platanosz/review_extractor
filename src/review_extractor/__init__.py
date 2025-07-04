import os
from .orchestrator import Orchestrator
from dotenv import load_dotenv
from .mongo_client import AtlasClient

load_dotenv()

twelve_labs_key = os.environ['TWELVE_LABS_KEY']
ATLAS_URI = os.environ['DB_URI']
DB_NAME = 'vidx'
VIDEO_METADATA = 'video_metadata'
ACCOUNT_DETAILS = 'account_details'

atlas_client = AtlasClient(ATLAS_URI, DB_NAME, VIDEO_METADATA, ACCOUNT_DETAILS)
orchestrator = Orchestrator(twelve_labs_key, atlas_client)