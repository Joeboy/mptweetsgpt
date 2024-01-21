from functools import cache
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from openai_query import get_openai_response
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

PROJECT_ROOT = Path(__file__).parent
DATA_ROOT = PROJECT_ROOT / "data"
TWEETS_BY_HANDLE_PATH = DATA_ROOT / "tweets_by_handle.json"
FULL_NAMES_BY_HANDLE_PATH = DATA_ROOT / "full_names_by_handle.json"
HTML_PATH = PROJECT_ROOT / "home.html"


class UserPrompt(BaseModel):
    """A prompt entered by a user"""

    topic: str
    twitter_handle: str


app = FastAPI()


@cache
def get_homepage_html() -> str:
    mps_options = "\n".join(
        f'<option value="{handle}">{full_name}</option>'
        for handle, full_name in get_full_names_by_handle().items()
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
def get_tweets_by_handle() -> dict[str, list[str]]:
    with TWEETS_BY_HANDLE_PATH.open() as f:
        return json.load(f)


@cache
def get_full_names_by_handle() -> dict[str, str]:
    with FULL_NAMES_BY_HANDLE_PATH.open() as f:
        return json.load(f)


class NoTweetsFoundException(Exception):
    pass


def get_tweets_for_handle(twitter_handle: str) -> list[str]:
    tweets_by_handle = get_tweets_by_handle()
    try:
        tweets_for_handle = tweets_by_handle[twitter_handle]
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
