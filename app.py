from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

BEARER_TOKEN = ""

@app.route("/", methods=["GET", "POST"])
def index():
    tweet_text = None  # Message shown on the page

    if request.method == "POST":
        # Step 1: Get the handle and date
        handle = request.form["handle"].lstrip("@").strip()  # Remove leading @
        date_str = request.form["date"].strip()

        # Step 2: Look up user ID
        user_id_url = f"https://api.twitter.com/2/users/by/username/{handle}"
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

        try:
            user_response = requests.get(user_id_url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            tweet_text = f"Error: Could not connect to Twitter API. ({e})"
            return render_template("home.html", tweet=tweet_text)

        if user_response.status_code != 200:
            tweet_text = f"Error: Twitter API returned status {user_response.status_code}"
            try:
                error_data = user_response.json()
                if "errors" in error_data:
                    tweet_text += f" - {error_data['errors'][0].get('detail', 'Unknown error')}"
            except Exception:
                pass
            return render_template("home.html", tweet=tweet_text)

        user_data = user_response.json()
        if "data" not in user_data:
            tweet_text = "User not found. Please check the handle."
            return render_template("home.html", tweet=tweet_text)

        user_id = user_data["data"]["id"]

        # Step 3: Parse date safely
        try:
            start_time = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            tweet_text = "Invalid date format. Use YYYY-MM-DD."
            return render_template("home.html", tweet=tweet_text)

        end_time = start_time + timedelta(days=1)

        # Step 4: Request tweets
        tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {
            "start_time": start_time.isoformat("T") + "Z",
            "end_time": end_time.isoformat("T") + "Z",
            "max_results": 10,  # Can go up to 100
            "tweet.fields": "created_at,text",
        }

        try:
            tweets_response = requests.get(
                tweets_url, headers=headers, params=params, timeout=10
            )
        except requests.exceptions.RequestException as e:
            tweet_text = f"Error: Could not connect to Twitter API. ({e})"
            return render_template("home.html", tweet=tweet_text)

        if tweets_response.status_code != 200:
            tweet_text = f"Error: Twitter API returned status {tweets_response.status_code}"
            try:
                error_data = tweets_response.json()
                if "errors" in error_data:
                    tweet_text += f" - {error_data['errors'][0].get('detail', 'Unknown error')}"
            except Exception:
                pass
            return render_template("home.html", tweet=tweet_text)

        tweets_data = tweets_response.json()
        if "data" in tweets_data and len(tweets_data["data"]) > 0:
            # Show the first tweet
            tweet_text = tweets_data["data"][0]["text"]
        else:
            tweet_text = "No tweets found on that date."

    return render_template("home.html", tweet=tweet_text)


if __name__ == "__main__":
    app.run(debug=True)
