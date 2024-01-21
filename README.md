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

* Figure out a way to update the tweet data. At the moment it's compiled from
  two files created with apify.com, which were apparently a struggle to
  generate and may still be incomplete
* We only have very basic tests. They currently talk to the real OpenAI API, maybe
  that's sort of OK but we might want to mock it at some point
* Make it look prettier
* Make the "spinner" indicator work properly
* List of MPs is a bit long for a static dropdown, maybe do an autocomplete?

## Credits

Thanks to:

* Matt for the [project](https://github.com/mattmegarry/prompt-ner)
  that provided the starting point. 
* Hannah for scraping the tweet data, and for running the hack day at which
  I did this.
