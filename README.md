Twitter Tweets
======

## Clone the Source

    # Clone Project repository
    git clone git@github.com:chandan9roy/twitter-tweet.git

## Configure It

    # Go to Project installation folder
    cd /home/twitter-tweet/

    # Virtual Envirnoment and requirements
    virtualenv -p /usr/bin/python3.5 env
    source env/bin/activate
    pip install -r requirements.txt


## Validate configurations

    ./manage.py check

## Migrate Database & Seed Default Data

    ./manage.py migrate

## Open python shell & create tweets in database
    ./manage.py shell_plus

    # In shell terminal:
    from tweets.views import get_twitter_tweets
    get_twitter_tweets(`search term`)
    example: get_twitter_tweets('gujrat election')
    exit shell

## Run local server

    ./manage.py runserver

## Go to following urls:
   # http://127.0.0.1:8000/tweets/
   # http://127.0.0.1:8000/export-tweets/
