from collections import defaultdict
from functools import cache
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from openai_query import get_openai_response
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

PROJECT_ROOT = Path(__file__).parent
DATA_ROOT = PROJECT_ROOT / "data"
TWEETS_PATH = DATA_ROOT / "dataset_twitter-scraper_2024-01-20_12-44-03-246.json"
HTML_PATH = PROJECT_ROOT / "home.html"


class UserPrompt(BaseModel):
    """A prompt entered by a user"""

    topic: str
    twitter_handle: str


app = FastAPI()


@cache
def get_homepage_html() -> str:
    mps_data, _ = get_mps_and_tweets()
    mps_data = mps_data[
        :800
    ]  # TODO: I think this is only needed because our dataset is not the correct one
    mps_options = "\n".join(
        f'<option value="{mp_data[0]}">{mp_data[1]}</option>' for mp_data in mps_data
    )
    template = HTML_PATH.read_text()
    return template.replace("__MPS_OPTIONS__", mps_options)


@app.get("/")
async def home():
    return HTMLResponse(
        content=get_homepage_html(),
        status_code=200,
    )


@cache
def get_mps_and_tweets() -> tuple:
    with open(TWEETS_PATH) as f:
        tweet_data = json.load(f)

    mps_data = list({tw["username"]: tw["fullname"] for tw in tweet_data}.items())

    tweets_by_twitter_handle = defaultdict(list)
    for tweet in tweet_data:
        if "text" in tweet:  # Some tweets don't have text, ie. images and maybe others?
            tweets_by_twitter_handle[tweet["username"]].append(tweet["text"])
    # print(f"{tweets_by_twitter_handle=}")
    return mps_data, tweets_by_twitter_handle


class NoTweetsFoundException(Exception):
    pass


def get_tweets_for_handle(twitter_handle: str) -> list[str]:
    # with (DATA_ROOT / "sultana_517.json").open() as f:
    #     data = json.load(f)
    # return [tw["text"] for tw in data if tw.get("text")]
    _, tweets_by_twitter_handle = get_mps_and_tweets()
    try:
        tweets_for_handle = tweets_by_twitter_handle[twitter_handle]
    except KeyError:
        raise NoTweetsFoundException(
            f"Couldn't find any tweets for twitter handle '{twitter_handle}'"
        )
    return tweets_for_handle


@app.post("/ask")
async def ask(user_prompt: UserPrompt):
    tweets_for_handle = get_tweets_for_handle(user_prompt.twitter_handle)
    tweets = "\n\n\n".join(
        f"{1 + i}: {tweet}" for i, tweet in enumerate(tweets_for_handle)
    )
    answer_text = get_openai_response(user_prompt.topic, tweets)
    if answer_text is None:
        raise HTTPException(
            status_code=404, detail="Did not get a response from openai"
        )
    answer_text = answer_text.replace("\n", "<br>\n\n")
    answer = f"""<div id="gpt-response"><p>We found <b>{len(tweets_for_handle)}</b> tweets for <b>{user_prompt.twitter_handle}</b>.
    We asked ChatGPT to summarize any statements about <b>{user_prompt.topic}</b>, and this is what it told us:</p>
    <p>{answer_text}</p></div>"""
    return HTMLResponse(content=answer, status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("web:app", host="0.0.0.0", port=8000, reload=True)
