# glide-health-llm

## 1. Installation
create a virtual env using pyenv or conda. then install depedency.
```sh
$ pip install -r requirements.txt
```
### Install redis
```sh
$ brew install redis
$ brew services start redis
```
### to get database url
1. download pgadmin (https://www.pgadmin.org/download/pgadmin-4-macos/)
2. create new database 
3. add database url in .env file.

### generate the github token 
1. go to https://github.com/settings/tokens 
2. generate find grained token for the specific repo and then pull request can be used for private repo

```sh
#.env
APP_SETTINGS='util.config.DevelopmentConfig'
OBJC_DISABLE_INITIALIZE_FORK_SAFETY='YES'
DATABASE_URL='postgresql://postgres:root@localhost:5432/llm_coder'
OPENAI_API_KEY = '<key>'
GITHUB_TOKEN = '<token>'
```

## 2. Setup

### Set up Migrations

```sha
$ flask db init
$ flask db migrate
$ flask db upgrade
```

### Run

Run each in a different terminal window...

```sh
# worker process (redis service should be on)
$ export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
$ python worker.py

# the app
$ flask --app app.py --debug run
```
# llm-flask
# llm-flask
"# ubantu-server" 
