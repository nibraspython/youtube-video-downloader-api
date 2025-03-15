from flask import Flask, request, jsonify
from pytube import YouTube
import re
import time
import random

app = Flask(__name__)

def get_video_url(url, resolution):
    try:
        # Random delay to avoid detection
        time.sleep(random.uniform(1, 3))  

        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()

        if stream:
            return stream.url, None  # Return direct video URL
        else:
            return None, "Video with the specified resolution not found."

    except Exception as e:
        return None, str(e)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
    return re.match(pattern, url) is not None

@app.route('/pvtyt', methods=['GET'])
def download_video():
    url = request.args.get('url')
    resolution = request.args.get('format', '360p')  # Default to 360p

    if not url:
        return jsonify({"error": "Missing 'url' parameter."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    video_url, error_message = get_video_url(url, resolution)

    if video_url:
        return jsonify({"download_url": video_url}), 200
    else:
        return jsonify({"error": error_message}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "API is alive!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
