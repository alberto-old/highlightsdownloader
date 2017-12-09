# Highlights Downloader

Simple application which downloads all the highlights stored in your Instapaper folders as Markdown files.

The downloader creates a tree of folders inside `highlights`. There will be one folder for each one you have in Instapaper. The folder name will be the id of the folder in Instapaper.

Inside every folder the downloader will create a Markdown file including the title of the bookmark, url reference and all the highlights (one paragraph per each of them).

## Requirements
Install the following packages:
- `pip install httplib2`
- `pip install oauth2`

## Usage

1. Get a KEY and SECRET OAuth from [Instapaper](https://www.instapaper.com/main/request_oauth_consumer_token)
2. Modify the file `Credentials.ini` with your KEY, SECRET, LOGIN and PASSWORD
3. Call the app `python downloader.py`

You can import then these Markdown files in your favourite Notes application e.g. [Bear](http://www.bear-writer.com/)

## Credits

Highlights Downloader makes use of a modified version of the [pyinstapaper library](https://github.com/mdorn/pyinstapaper) Python wrapper to the Instapaper API; thanks [Matt Dorn](https://github.com/mdorn)!
