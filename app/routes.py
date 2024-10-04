import uuid
from flask import Blueprint, request, send_file, send_from_directory, jsonify
from . import socketio
from .services import start_image_scrape, delete_temp_files
from .shared import zip_files
import os

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def serve_react(path):
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/dist'))
    
    print(f'checking path {path}, got {os.path.join(dist_dir, path)}')
    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)

    return send_from_directory(dist_dir, 'index.html')

@main.route('/api/zip_files', methods=['GET'])
def get_zip_files():
    return(jsonify(zip_files))

@main.route('/api/mgn-scraper', methods=['POST'])
def start_mgn_scrape():
    print("Form Submitted")
    print(request.json)
    data = request.json.get('data')
    sid = request.json.get('sid')
    if not sid:
        return 'No sid provided', 400
    if not data:
        return 'No data provided', 400
    
    image_ids = data.split(',')
    image_ids = [image_id.strip() for image_id in image_ids]

    task_id = str(uuid.uuid4())
    socketio.start_background_task(start_image_scrape, sid, image_ids, task_id)

    return jsonify({'message': 'Scraping started successfully'}), 200

@main.route('/api/download/<filename>', methods=['GET'])
def download(task_id):
    zip_path = zip_files[task_id]
    if not zip_path or not os.path.exists(zip_path):
        return jsonify({'message': 'File not found'}), 404
    response = send_file(zip_path, as_attachment=True, attachment_filename='images.zip')
    delete_temp_files(zip_path)
    
    return response