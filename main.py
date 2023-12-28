# app.py
from flask import Flask, request, jsonify
from requests_html import HTMLSession

app = Flask(__name__)

@app.route('/get_link')
def get_link():
    initial_url = request.args.get('url')
    if not initial_url:
        return jsonify({"error": "No URL provided."}), 400

    session = HTMLSession()
    try:
        response = session.get(initial_url)
        response.html.render(sleep=1)

        first_link = response.html.find('a.btn-primary', first=True)
        if first_link:
            first_href = first_link.attrs['href']
            download_response = session.get(first_href)
            if download_response.status_code == 200:
                first_link = download_response.html.find('a.btn.btn-success.btn-lg.h6', first=True)
                if first_link:
                    first_href = first_link.attrs['href']
                    return jsonify({"streaming_link": first_href})
                else:
                    return jsonify({"error": "Streaming link not found."}), 404
            else:
                return jsonify({"error": f"Failed to retrieve content, status code: {download_response.status_code}"}), download_response.status_code
        else:
            return jsonify({"error": "No first link found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
