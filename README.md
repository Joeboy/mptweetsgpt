# MPTweetsGPT

This is an interface to OpenAI's gpt-4 api. The idea is, a user can select an
MP and a question to ask and we'll ask ChatGPT to summarize any relevant info
found in the MP's recent tweets.

You'll need an OpenAI API key with access to gpt4 - specifically the gpt-4-1106-preview
model.

To run it locally:

* Get an OpenAI API key
* Copy `config_template.py` to `config.py`, and edit it to include your API key
* In the project's root folder, run `python -m venv venv`
* Activate the venv with `. venv/bin/activate`
* `pip install -r requirements.txt`
* `python web.py`
* In a web browser, go to [http://localhost:8000](http://localhost:8000)

To deploy it:

* `uvicorn web:app --host 0.0.0.0 --port 8000`
* Configure a webserver like nginx to handle tls and proxy the uvicorn port

## TODO

* We still need a full scrape of the twitter data (Hannah is working on this)
* We only have very basic tests. They currently talk to the real OpenAI API, maybe
  that's sort of OK but we might want to mock it at some point
* Make it look prettier
* Make the "spinner" indicator work properly
* List of MPs is too long for a static dropdown, do an autocomplete
* In fact right now the html / js is a complete mess