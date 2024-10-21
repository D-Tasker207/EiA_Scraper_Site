import zipfile
import os
import time
import shutil
import threading
from app.socketio_handlers import Progress

def create_zip_file(sid, temp_dir):
    zip_path = os.path.join(temp_dir, "images.zip")
    total_files = len(os.listdir(temp_dir))
    progress_tracker = Progress(sid, total_files + 1)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for  root, _, files in os.walk(temp_dir):
            for i, file in enumerate(files):
                if file == "images.zip":
                    continue
                progress_tracker.update(f"{i+1}/{total_files}: Zipping {file}")
                zipf.write(os.path.join(root, file), file)

    progress_tracker.update("Zipping complete")
    return zip_path

def delete_temp_files(zip_files, task_id, delay=30):
    def delayed_delete():
        print(f"Waiting {delay} seconds to delete {task_id} files")
        time.sleep(delay)
        zip_path = zip_files.pop(task_id, None)
        if zip_path:
            temp_dir = os.path.dirname(zip_path)
            shutil.rmtree(temp_dir)
            print(f"Deleted {temp_dir} for task {task_id}")
    threading.Thread(target=delayed_delete).start()