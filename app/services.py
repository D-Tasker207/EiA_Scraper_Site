from .socketio_handlers import send_message, send_url, client_disconnect
from app.tasks.mgn_scraper import get_images
from app.tasks.utils import create_zip_file, delete_temp_files
from .shared import zip_files
import os
import shutil
import threading
import time

def start_image_scrape(sid, image_ids, task_id):
    send_message(sid, "Starting image scrape")
    zip_path = get_images(sid, image_ids)
    zip_path = create_zip_file(sid, zip_path)

    zip_files[task_id] = zip_path

    download_url = f"/api/download/{task_id}"
    send_url(sid, download_url)
    client_disconnect(sid)