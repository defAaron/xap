from flask import Flask, render_template, request

import requests

from datetime import datetime, timedelta

app = Flask(__name__)

bearer_token = ""

def get_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    return None

def tweet_date(username, date_str):
    user_id = get_id(username)
    if not user_id:
        return "Sorry, we couldn't find that user. Womp womp : ("

    start_time = datetime.strptime(date_str, "%Y-%m-%d")
    end_time = start_time + timedelta(days=1)

    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {
        "start_time": start_time.isoformat("T") + "Z",
        "end_time": end_time.isoformat("T") + "Z",
        "max_results": 5,
        "tweet.fields": "created_at,text"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        tweets = response.json().get("data", [])
        if tweets:
            return tweets[0]['text']
        else:
            return "This user did not make any tweets on this date! Try entering a different date to see their tweets : )"
    else:
        return f"Error: {response.status_code}"

@app.route('/', methods=['GET', 'POST'])
def index():
    tweet = None
    error = None
    if request.method == 'POST':
        handle = request.form.get('handle').strip()
        date = request.form.get('date').strip()
        tweet = tweet_date(handle, date)
    return render_template('index.html', tweet=tweet)

if __name__ == '__main__':
    app.run(debug=True)