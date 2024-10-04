import zipfile
import os
from app.socketio_handlers import Progress, send_error

def create_zip_file(sid, temp_dir):
    zip_path = os.path.join(temp_dir, "images.zip")
    progress_tracker = Progress(sid, len(os.listdir(temp_dir))-1)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file == "images.zip":
                    continue
                progress_tracker.update(f"Zipping {file}")
                zipf.write(os.path.join(root, file), file)

    return zip_path
    
