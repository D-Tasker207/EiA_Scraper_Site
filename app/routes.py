from flask import Blueprint, request, send_file, send_from_directory, jsonify
from .socketio_handlers import socketIO
from .services import start_image_scrape
import os

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def serve_react(path):
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/dist'))

    print(f'checking path {path}, got {os.path.exists(os.path.join(dist_dir, path))}')
    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)

    return send_from_directory(dist_dir, 'index.html')

@main.route('/static-test')
def serve_static():
    return send_from_directory('../static/dist', 'bundle.js')

@main.route('/api/mgn_scrape', methods=['POST'])
def start_mgn_scrape():
    data = request.json.get('data')
    if not data:
        return 'No data provided', 400

    image_ids = data.get('image_ids').split(',')
    image_ids = [image_id.strip() for image_id in image_ids]
    sid = request.sid

    start_image_scrape(sid, image_ids)

    return jsonify({'message': 'Scraping started successfully'}), 200

@main.route('/api/download/<filename>', methods=['GET'])
def download(filename):
    zip_path = f"/tmp/{filename}.zip"
    if not os.path.exists(zip_path):
        return jsonify({'message': 'File not found'}), 404
    
    return send_file(zip_path, as_attachment=True)