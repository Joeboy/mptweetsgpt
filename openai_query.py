from openai import OpenAI
from config import OPENAI_API_KEY


def get_openai_response(topic: str, tweets: str) -> str | None:
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    prompt = f"""
    Here's a list of tweets from a UK MP:

    {tweets}

    Based on these tweets, please provide a response to the following question:

    {topic}
    """
    # print(f"{prompt=}")
    # """
    # Based on these tweets, what does this person think about {topic}
    # """
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-1106-preview",
    )

    return completion.choices[0].message.content
