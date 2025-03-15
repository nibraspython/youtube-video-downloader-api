from flask import Flask, request, jsonify
from pytube import YouTube
import re
import random
import requests
from requests.exceptions import ProxyError, ConnectTimeout

app = Flask(__name__)

# List of free proxies (update regularly)
PROXIES = [
    "http://138.201.132.168:3128",
    "http://95.216.65.69:3128",
    "http://103.155.54.26:8080",
    "http://89.58.12.202:3128"
]

def get_random_proxy():
    """Returns a random proxy from the list"""
    proxy = random.choice(PROXIES)
    return {"http": proxy, "https": proxy}

def get_video_info(url):
    try:
        proxy = get_random_proxy()
        response = requests.get(url, proxies=proxy, timeout=10)  # Increased timeout
        
        yt = YouTube(url)
        video_info = {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "description": yt.description,
            "publish_date": str(yt.publish_date),
        }
        return video_info, None
    except (ProxyError, ConnectTimeout) as e:
        return None, f"Proxy error or connection timeout: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
    return re.match(pattern, url) is not None

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
