"""Getting a proper list of MPs' tweets is a bit of a work in progress. We
currently have two json files, which include a lot of non-MP tweets. Let's
combine them, clean them up and export the result into a new file."""
from collections import defaultdict
import json
import csv
from pathlib import Path

DATA_ROOT = Path(__file__).parent / "data"


def process():
    with (DATA_ROOT / "MPsonTwitter_list_name.csv").open() as f:
        reader = csv.DictReader(f)
        full_names_by_handle = {row["Screen name"]: row["Name"] for row in reader}
    full_names_by_handle = dict(
        sorted(full_names_by_handle.items(), key=lambda x: x[1])
    )

    with (
        DATA_ROOT / "dataset_twitter-scraper_2024-01-20_12-44-03-246.json"
    ).open() as f:
        data = json.load(f)
    with (DATA_ROOT / "dataset_tweet-flash_2024-01-20_16-07-32-791.json").open() as f:
        data2 = json.load(f)

    # The data files contain tweets from non-MPs (retweets?), so:
    data = [t for t in data if t["username"] in full_names_by_handle.keys()]
    data2 = [t for t in data2 if t["username"] in full_names_by_handle.keys()]

    # Combine the files, omitting any duplicated tweets:
    data_tweet_ids = [tw["id"] for tw in data]
    data.extend((tw for tw in data2 if tw["tweet_id"] not in data_tweet_ids))

    # Map each twitter handle to a list of tweets
    tweets_by_handle = defaultdict(list)
    for tw in data:
        if tw.get("text"):  # Not all tweets have text
            tweets_by_handle[tw["username"]].append(tw["text"])

    with (DATA_ROOT / "full_names_by_handle.json").open("w") as f:
        json.dump(full_names_by_handle, f)

    with (DATA_ROOT / "tweets_by_handle.json").open("w") as f:
        json.dump(tweets_by_handle, f)


if __name__ == "__main__":
    process()
