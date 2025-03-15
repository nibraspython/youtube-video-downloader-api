from flask import Flask, request, jsonify
from pytube import YouTube
import re

app = Flask(__name__)

def get_video_url(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if stream:
            return stream.url, None  # Return direct URL instead of downloading
        else:
            return None, "Video with the specified resolution not found."
    except Exception as e:
        return None, str(e)

def get_video_info(url):
    try:
        yt = YouTube(url)
        video_info = {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "description": yt.description,
            "publish_date": yt.publish_date,
        }
        return video_info, None
    except Exception as e:
        return None, str(e)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
    return re.match(pattern, url) is not None

@app.route('/')
def home():
    return jsonify({'message': 'YouTube Downloader API is running!'}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "API is alive!"}), 200

@app.route('/pvtyt', methods=['GET', 'POST'])
def download_youtube_video():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url')
        resolution = data.get('resolution', '360p')  # Default to 360p

    elif request.method == 'GET':
        url = request.args.get('url')
        resolution = request.args.get('resolution', '360p')  # Get resolution from URL params

    if not url:
        return jsonify({"error": "Missing 'url' parameter."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400
    
    video_url, error_message = get_video_url(url, resolution)
    
    if video_url:
        return jsonify({"download_url": video_url}), 200
    else:
        return jsonify({"error": error_message}), 500

@app.route('/download/<resolution>', methods=['POST'])
def download_by_resolution(resolution):
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400
    
    video_url, error_message = get_video_url(url, resolution)
    
    if video_url:
        return jsonify({"download_url": video_url}), 200
    else:
        return jsonify({"error": error_message}), 500

@app.route('/video_info', methods=['POST'])
def video_info():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400
    
    video_info, error_message = get_video_info(url)
    
    if video_info:
        return jsonify(video_info), 200
    else:
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
