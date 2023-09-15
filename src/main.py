from flask import Flask, request, jsonify, Response, render_template, send_from_directory
import sqlite3, base64, os, json, secrets
import requests # For Google's safebrowsing API
import validators

try:
	RESOURCE_ROOT = os.environ["RESOURCE_ROOT"]
except KeyError:
	RESOURCE_ROOT = os.getcwd()

TEMPLATE_DIRECTORY = f"{RESOURCE_ROOT}/templates"
STATIC_DIRECTORY   = f"{RESOURCE_ROOT}/static"
DATABASE_FILE      = f"{RESOURCE_ROOT}/database.db"

try:
	GOOGLE_SAFEBROWSING_API_KEY = os.environ["GOOGLE_SAFEBROWSING_API_KEY"]
except KeyError:
	print("[WARNING] Will not do safebrowsing check! Try setting the GOOGLE_SAFEBROWSING_API_KEY environment variable!")
	GOOGLE_SAFEBROWSING_API_KEY = None

app = Flask(
	__name__
	, static_url_path=''
	, static_folder=STATIC_DIRECTORY
	, template_folder=TEMPLATE_DIRECTORY
)

def gen_uid(curs):
	uid = secrets.token_urlsafe(8)
	# Ensure uniqueness
	while curs.execute("select * from redirects where id = ?", uid).fetchone() is not None:
		uid = secrets.token_urlsafe(8)
	return uid

def get_client_ip():
	# Get the IP if not behind a proxy
	if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
		return request.environ["REMOTE_ADDR"]
	# Get the IP if behind a proxy
	return request.environ["HTTP_X_FORWARDED_FOR"]

def validate_url(url):
	if not validators.url(url):
		return False, "Malformed URL"
	elif GOOGLE_SAFEBROWSING_API_KEY is None:
		print(f"[WARNING]: Cannot check safebrowsing for {url}!")
		return True, "Cannot check for malware"
	return True, "TODO" # TODO

@app.get("/")
@app.get("/create")
def get_create_page():
	return render_template("create.html", created=False, error=False)

@app.post("/create")
def create_shortened_url():
	# Support JSON and form
	body = request.form
	if not "url" in body or body["url"].strip() == "":
		return render_template("create.html", url=None, created=False, error=True, error_body="'url' field in request was empty!")
	long_url = body["url"]
	valid_url, message = validate_url(long_url)
	print(valid_url, message)
	if not valid_url:
		return render_template("create.html", url=None, created=False, error=True, error_body=message)
	print(f"[MESSAGE] Creating short url for '{long_url}'")
	url = "https://kernel.org"
	return render_template("create.html", url=url, created=True, error=False)

@app.get("/l/<uid>")
def get_redirect_page(uid):
	connection = sqlite3.connect(DATABASE_FILE)
	curs = connection.cursor()
	# Python's sqlite module sanitizes input automatically if you use
	# this syntax
	result = curs.execute("select url from redirects where id = ?", (uid,)).fetchone()
	connection.commit()
	if result is None:
		return render_template("error.html", error_body=f"The link ID {uid} is not in our database")
	url = "https://kernel.org"
	return render_template("redirect.html", url=url)

