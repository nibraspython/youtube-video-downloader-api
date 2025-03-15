from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

def get_video_url(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if stream:
            return stream.url, None  # Return direct download URL
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
            "publish_date": yt.publish_date.strftime("%Y-%m-%d"),
            "thumbnail": yt.thumbnail_url
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

@app.route('/pvtyt', methods=['GET'])
def download_youtube_video():
    url = request.args.get('url')
    resolution = request.args.get('resolution', '360p')

    if not url:
        return jsonify({"error": "Missing 'url' parameter."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    video_url, error_message = get_video_url(url, resolution)

    if video_url:
        return jsonify({"download_url": video_url}), 200
    else:
        return jsonify({"error": error_message}), 500

@app.route('/video_info', methods=['GET'])
def video_info():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' parameter."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    video_info, error_message = get_video_info(url)

    if video_info:
        return jsonify(video_info), 200
    else:
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
