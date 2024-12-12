import http.client
import json
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# API Route
@app.route('/detect_x', methods=['POST'])
def detect_x():
    # Parse JSON from request
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'error': 'Username is required.'}), 400

    username = data.get('username')
    # Fetch user details
    output = fetch_user_details(username)
    if output is None:
        return jsonify({'error': 'Failed to fetch user details.'}), 500

    return jsonify({'result': output})

# API Connection Setup
headers = {
    'x-rapidapi-key': "5d54c973b7msh2418c169d4909b0p1e5362jsn1123fc1cd8ae",
    'x-rapidapi-host': "twitter-api47.p.rapidapi.com"
}

def fetch_user_details(username):
    try:
        conn = http.client.HTTPSConnection("twitter-api47.p.rapidapi.com")
        conn.request("GET", f"/v2/user/by-username?username={username}", headers=headers)
        res = conn.getresponse()
        
        if res.status != 200:
            print(f"Error: Received status code {res.status}")
            return None

        data = json.loads(res.read().decode("utf-8"))

        # Map user details
        selected_fields = {
            'Username': data.get('legacy', {}).get('name'),
            'Name': data.get('legacy', {}).get('screen_name'),
            'Bio': data.get('legacy', {}).get('description'),
            'Followers': data.get('legacy', {}).get('normal_followers_count'),
            'Following': data.get('legacy', {}).get('friends_count'),
            'Verified': data.get('is_blue_verified'),
            'AccountPrivacy': data.get('verification_info', {}).get('is_identity_verified'),
            'ProfileImage': data.get('legacy', {}).get('profile_image_url_https'),
            'NumberOfPosts': data.get('legacy', {}).get('media_count'),
            'SocialMediaSite': "Twitter",
        }
        return selected_fields

    except Exception as e:
        print(f"Error fetching user details: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
