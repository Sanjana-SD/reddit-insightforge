import requests
import json
import os
from datetime import datetime


HEADERS = {
    "User-Agent": "reddit-insightforge-data-engineering-project"
}


def fetch_subreddit(subreddit, limit=50):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_posts(raw_json, subreddit):
    posts = []

    children = raw_json["data"]["children"]

    for item in children:
        data = item["data"]

        post = {
            "post_id": data.get("id"),
            "title": data.get("title"),
            "author": data.get("author"),
            "created_utc": data.get("created_utc"),
            "score": data.get("score"),
            "num_comments": data.get("num_comments"),
            "subreddit": subreddit,
            "selftext": data.get("selftext"),
            "url": data.get("url")
        }

        posts.append(post)

    return posts


def save_bronze(posts, subreddit):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    path = os.path.join("data", "bronze", subreddit, today)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(
        path,
        f"reddit_{datetime.utcnow().strftime('%H%M%S')}.json"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    print(f"Saved {len(posts)} posts to {file_path}")


def main():
    subreddits = ["datascience", "machinelearning", "programming"]

    for sub in subreddits:
        raw = fetch_subreddit(sub)
        posts = parse_posts(raw, sub)
        save_bronze(posts, sub)


if __name__ == "__main__":
    main()
