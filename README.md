# USU URL Shortener

URL shortener for use on USU campus. Developed for the Free Software and Linux Club.

Please set the following environment variables before running:

`RESOURCE_ROOT`: the root directory of this project (assumes cwd if not)

To run (developer):

```sh
# in main folder
export RESOURCE_ROOT=$(pwd)
cd src
export FLASK_APP=main
flask run
```

Please first install the requirements in `requirements.txt`
