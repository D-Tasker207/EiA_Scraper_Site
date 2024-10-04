from .socketio_handlers import send_message, send_url, client_disconnect
from tasks.mgn_scraper import get_images
from tasks.zip_files import create_zip_file
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

def delete_temp_files(task_id, delay=30):
    def delayed_delete():
        time.sleep(delay)
        zip_path = zip_files.pop(task_id, None)
        if zip_path:
            temp_dir = os.path.dirname(zip_path)
            shutil.rmtree(temp_dir)
            print(f"Deleted {temp_dir} for task {task_id}")
    threading.Thread(target=delayed_delete).start()