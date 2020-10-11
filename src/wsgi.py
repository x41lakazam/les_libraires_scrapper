#!/usr/local/bin/python3
#
# results.py
# src
#
# Created by Eyal Shukrun on 10/12/20.
# Copyright 2020. Eyal Shukrun. All rights reserved.
#
import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "See results <a href='/results'>here</a>"

@app.route('/results')
def result():
    return open("results.csv", 'r').read()

if __name__ == "__main__":
    app.run(port=5001)
