#!/bin/bash

export FLASK_APP=wsgi.py
kill -9 $(lsof -t -i tcp:5000)
flask run & scrapyd
