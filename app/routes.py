from flask import Blueprint, request, send_file, send_from_directory, jsonify
from .socket import socketio
from .services import start_image_scrape
import os

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join('static/dist', path)):
        return send_from_directory('static/dist', path)
    return send_from_directory('static/dist', 'index.html')
    

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