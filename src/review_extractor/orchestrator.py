
import boto3
import os
import logging
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task
from .mongo_client import AtlasClient
from datetime import datetime, timezone
from moviepy import VideoFileClip

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(asctime)s [%(filename)s:%(lineno)d]: %(message)s'
                    )
logger = logging.getLogger(__name__)


class Orchestrator:

    def __init__(self, api_key: str, atlas_client: AtlasClient):
        self.client = TwelveLabs(api_key=api_key)
        self.atlas_client = atlas_client
        self.s3 = boto3.client('s3')

    def start(self, record: dict) -> dict:
        
        logger.info("start")
        bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        logger.info(f"Processing file from bucket: {bucket}, key: {s3_key}")
        # TODO algorithm to extract metadata from the video
        # 1. Download the file from S3
        file, file_path = self.get_file(bucket, s3_key)
        duration = self.get_video_duration_moviepy(file_path)
        # 2. Retrived current video metadata from MongoDB
        video_metadata = self.atlas_client.find_video_metadata(s3_key)
        logger.info(f"Video metadata: {video_metadata}")
        # 3. Check if video index already exists in MongoDB
        account_details = self.atlas_client.find_account_details(video_metadata['discord_id'])
        index_id = account_details.get("index_id")
        if index_id == None:
            models = [
                {
                    "name": "pegasus1.2",
                    "options": ["visual", "audio"]
                }
            ]
        #   3-a. If not, create a new video index
            index = self.client.index.create(name=video_metadata["discord_id"], models=models)
            print(f"Index created: id={index.id}, name={index.name}")
        #   3-b. Stored index in MongoDB
            self.atlas_client.upsert_index_id(video_metadata["discord_id"], index.id)
            index_id = index.id
        # 4. Process the video using Twelve Labs API
        task = self.client.task.create(index_id=index_id, file=file)
        # print(f"Task id={task.id}, Video id={task.video_id}")
        # task.wait_for_done(sleep_interval=5, callback=self.on_task_update)
        # if task.status != "ready":
        #     raise RuntimeError(f"Indexing failed with status {task.status}")
        # print(f"The unique identifier of your video is {task.video_id}.")
        video_id = task.video_id
        task_id = task.id
        # 5. Trigger prompts to extract metadata
        prompts = account_details.get("prompts", [])
        # for prompt in account_details.get("prompts", []):
        #     text_stream = self.client.analyze_stream(
        #     video_id=video_id, prompt=prompt.get("prompt_content"), temperature=0.2)
        #     for text in text_stream:
        #         print(text)
        #     print(f"Aggregated text: {text_stream.aggregated_text}")
        #     prompts.append({prompt.get("prompt_name"): text_stream.aggregated_text})
        # 6. Store the metadata in MongoDB (video_id, index_id, metadata, processed_timestamp, duration, etc.)
        self.atlas_client.update_video_metadata(s3_key,
                                                {"task_id": task_id,
                                                 "video_id": video_id,
                                                 "status":"INDEXING",
                                                 "index_id": index_id,
                                                 "prompts":prompts,
                                                 "duration": f"{duration} seconds",
                                                 "updated_at": datetime.now(timezone.utc)}
                                                )
        
        # TODO
        # create a separate collection for each client account and what their preferences are
        # Add pymovie to extract video duration
        # increase memory for lambda functions to handle video sizes
        # two use cases:
        #   1. clips to be processed to montage videos
        #   2. long videos to be processed to short videos

        # 2. Download file to /tmp

        # Optionally: clean up file
        # self.atlas_client.find_video_metadata(s3_key)

        os.remove(file_path)     
        return {"video_id": video_id, "index_id": index_id, "key_s3": s3_key}

    def get_file(self, bucket, key):
        file_name = key.split('/')[-1]
        local_path = f'/tmp/{file_name}'
        self.s3.download_file(bucket, key, local_path)
        logger.info(f"Downloaded {key} to {local_path}")

        # 3. Process the file (your logic here)
        # Example: Just print size, but here you could use ffmpeg, analyze, etc.
        return open(local_path, 'rb'), local_path
            # return {'file': (file_name, f)}
        
    def on_task_update(self, task: Task):
        print(f"  Status={task.status}")
        
    def get_video_duration_moviepy(self, filename):
        """
        Retrieves the duration of a video file using MoviePy.

        Args:
            filename (str): The path to the video file.

        Returns:
            float: The duration of the video in seconds.
        """
        try:
            clip = VideoFileClip(filename)
            duration = clip.duration
            clip.close()  # Release resources
            return duration
        except Exception as e:
            print(f"Error getting video duration with MoviePy: {e}")
            return None

