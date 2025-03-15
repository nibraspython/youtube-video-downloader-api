import requests
from flask import Flask, request, jsonify
from pytube import YouTube
import random
import time

app = Flask(__name__)

# List of working proxies (Replace with fresh proxies)
PROXIES = [
    "138.201.132.168:3128",
    "95.216.65.69:3128",
    "103.155.54.26:8080",
    "89.58.12.202:3128"
]

def get_random_proxy():
    """Returns a random proxy from the list"""
    proxy = random.choice(PROXIES)
    return {"http": f"http://{proxy}", "https": f"https://{proxy}"}

def get_video_url(url, resolution):
    try:
        time.sleep(random.uniform(1, 3))  # Random delay to avoid detection

        proxy = get_random_proxy()  # Get a proxy

        # Make a request through the proxy to check if it works
        try:
            response = requests.get("https://www.youtube.com", proxies=proxy, timeout=5)
            if response.status_code != 200:
                return None, "Proxy failed, try again."
        except requests.exceptions.RequestException:
            return None, "Proxy connection error, try again."

        yt = YouTube(url, proxies=proxy)  # Use proxy for pytube
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
