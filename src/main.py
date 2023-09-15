from flask import Flask, request, jsonify, Response, render_template, send_from_directory
import sqlite3, base64, os, json, secrets
import requests # For Google's safebrowsing API
from urlparse import urlparse

try:
	RESOURCE_ROOT = os.environ["RESOURCE_ROOT"]
except KeyError:
	RESOURCE_ROOT = os.getcwd()

TEMPLATE_DIRECTORY = f"{RESOURCE_ROOT}/templates"
STATIC_DIRECTORY = f"{RESOURCE_ROOT}/static"

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
	if GOOGLE_SAFEBROWSING_API_KEY is None:
		print(f"[WARNING]: Cannot check safebrowsing for {url}!")
		return True
	return True # TODO

@app.get("/")
@app.get("/create")
def get_create_page():
	return render_template("create.html", created=False, error=False)

@app.post("/create")
def create_shortened_url():
	# Support JSON and form
	body = request.form
	if not "url" in body or body["url"].strip() == "":
		render_template("create.html", url=None, created=False, error=True, error_body="'url' field in request was empty!")
	long_url = body["url"]
	print(type(long_url))
	print(f"[MESSAGE] Creating short url for '{long_url}'")
	url = "https://kernel.org"
	return render_template("create.html", url=url, created=True, error=False)

@app.get("/l/<uid>")
def get_redirect_page(uid):
	url = "https://kernel.org"
	return render_template("redirect.html", url=url)

