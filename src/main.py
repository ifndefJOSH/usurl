from flask import Flask, request, jsonify, Response, render_template, send_from_directory
import sqlite3, base64, os, json, secrets

TEMPLATE_DIRECTORY = f"{os.getcwd()}/templates"
STATIC_DIRECTORY = f"{os.getcwd()}/static"

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

