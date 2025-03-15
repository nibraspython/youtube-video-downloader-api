import requests
from flask import Flask, request, jsonify
from pytube import YouTube
import random
import time

app = Flask(__name__)

# Free proxy list (Update with fresh proxies)
PROXIES = [
    "http://138.201.132.168:3128",
    "http://95.216.65.69:3128",
    "http://103.155.54.26:8080",
    "http://89.58.12.202:3128"
]

def get_random_proxy():
    """Returns a random proxy from the list"""
    return {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}

def get_video_url(url, resolution):
    try:
        time.sleep(random.uniform(1, 3))  # Random delay to avoid detection

        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()

        if stream:
            return stream.url, None
        else:
            return None, "Video with the specified resolution not found."

    except Exception as e:
        return None, str(e)

@app.route('/pvtyt', methods=['GET'])
def download_video():
    url = request.args.get('url')
    resolution = request.args.get('format', '360p')  # Default to 360p

    if not url:
        return jsonify({"error": "Missing 'url' parameter."}), 400

    proxy = get_random_proxy()

    try:
        # Send request through proxy
        response = requests.get(url, proxies=proxy, timeout=5)
        if response.status_code != 200:
            return jsonify({"error": "Proxy failed, try again."}), 500

    except requests.exceptions.RequestException:
        return jsonify({"error": "Proxy connection error, try again."}), 500

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
