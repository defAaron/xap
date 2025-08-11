from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Put your Bearer Token here
BEARER_TOKEN = 'YOUR_BEARER_TOKEN_HERE'

@app.route('/', methods=['GET', 'POST'])
def index():
    tweet_text = None  # This will store the tweet or message

    if request.method == 'POST':
        # Step 1: Get the handle and date from the form
        handle = request.form['handle'].strip()
        date_str = request.form['date'].strip()

        # Step 2: Find the user ID from the handle
        user_id_url = f"https://api.twitter.com/2/users/by/username/{handle}"
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        user_response = requests.get(user_id_url, headers=headers)

        if user_response.status_code != 200:
            tweet_text = "Error: Could not find the user."
        else:
            user_data = user_response.json()
            if "data" not in user_data:
                tweet_text = "User not found."
            else:
                user_id = user_data["data"]["id"]

                # Step 3: Prepare the start and end time for that date
                try:
                    start_time = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    tweet_text = "Invalid date format."
                    return render_template('home.html', tweet=tweet_text)

                end_time = start_time + timedelta(days=1)

                # Step 4: Request the tweets for that date
                tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
                params = {
                    "start_time": start_time.isoformat("T") + "Z",
                    "end_time": end_time.isoformat("T") + "Z",
                    "max_results": 5,
                    "tweet.fields": "created_at,text"
                }

                tweets_response = requests.get(tweets_url, headers=headers, params=params)

                if tweets_response.status_code != 200:
                    tweet_text = "Error fetching tweets."
                else:
                    tweets_data = tweets_response.json()
                    if "data" in tweets_data and len(tweets_data["data"]) > 0:
                        # Step 5: Take the first tweet from that day
                        tweet_text = tweets_data["data"][0]["text"]
                    else:
                        tweet_text = "No tweet on that date."

    return render_template('home.html', tweet=tweet_text)

if __name__ == '__main__':
    app.run(debug=True)
