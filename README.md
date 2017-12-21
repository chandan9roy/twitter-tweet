Twitter Tweets
======

# Important Notes

This guide is long because it covers many cases and includes all commands you need.

This installation guide was created for and tested on **Ubuntu 16.04** operating systems.

This is the official installation guide to set up a production server. To set up a **development installation** and to contribute read `Contributing.md`.

The following steps have been known to work. Please **use caution when you deviate** from this guide. Make sure you don't violate any assumptions twitter tweets makes about its environment.


## Packages / Dependencies

Run following commands

    sudo apt-get update
    sudo apt-get -y upgrade

**Note:** During this installation some files will need to be edited manually. If you are familiar with vim set it as default editor with the commands below. If you are not familiar with vim please skip this and keep using the default editor.


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

    ./manage.py validate

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
