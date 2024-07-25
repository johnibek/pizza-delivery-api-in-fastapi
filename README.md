# README
## SETUP

#### Create virtual environment and activate it
    `python3 -m venv venv`

###### Linux / Mac
    source venv/bin/activate

###### Windows
    .\venv\Scripts\activate

#### Install requirements

    pip install -r requirements.txt

#### Create an `.env` file inside `app` directory. Content should look like the following

    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_PASSWORD=your_db_password
    DATABASE_NAME=db_name
    DATABASE_USERNAME=db_username
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60

#### Generating secret key
    openssl rand -hex 32


## URL for api docs in swagger:
http://127.0.0.1:8000/docs

