# FastAPI and JWTs

----------

Using FastAPI and MongoDB Atlast to create a Post Creation App.
Tutorial link - [here](https://youtu.be/0_seNFCtglk)

----------

## Setup Instructions

- Clone the Git Repository using `git clone`
- Switch to diretory
- Create a virtual environment using command `python3 -m venv env`
- Activate the environment by `source env/bin/activate`
- Install pip dependecies `pip install -r requirements.txt'
- Run the command `echo "secret = $(python3 -c 'import secrets;print(secrets.token_hex(16))')\nalgorithm = HS256\nmongodb_uri = \nmongodb_db = posts_application" > .env`
- Edit the `.env` file and fill in the mongodb uri details
- Run the program using the command `uvicorn main:app --reload`
- Visit <http://localhost:8000/docs> for the interactive API Doc
