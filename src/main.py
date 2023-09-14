from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import sqlite3, base64, os

app = FastAPI()

def genUid(curs):
	uid = base64.b64encode(os.urandom(32))[:8].decode("utf-8")
	# Ensure uniqueness
	while curs.execute("select * from redirects where id = ?", uid).fetchone() is not None:
		uid = base64.b64encode(os.urandom(32))[:8].decode("utf-8")
	return uid

def authenticate(token : str):
	# TODO: authenticate via Oath tokens
	return False

# Endpoint for accessing links
@app.get("/{link_id}")
async def redirect(link_id : str):
	connection = sqlite3.connect("linkurls.db")
	curs = connection.cursor()
	# Python's sqlite module sanitizes input automatically if you use
	# this syntax
	result = curs.execute("select url from redirects where id = ?", (link_id,)).fetchone()
	connection.commit()
	if result is None:
		return HTMLResponse(status_code=HTTP_404_NOTFOUND,
				content=f"""<HTML>
<head>
<title>Not Found</title>
</head>
<body>
<h1>The shortened URL {link_id} is not known!</h1>
</body>
""")
	redirect_url = result[0]
	return RedirectResponse(
			redirect_url
			, status_code=status.HTTP_303_SEEOTHER
		)

@app.post("/create")
async def create(request : Request):
	json = await request.json()
	token = json["token"]
	if not authenticate(token):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED
			, detail="You are not authorized to create redirects on this server!"
		)
	connection = sqlite3.connect("linkurls.db")
	curs = connection.cursor()
	uid = genUid(curs)
	curs.execute("insert into redirects (url, id) values (?, ?)", (json["url"], uid,))
	connection.commit()


