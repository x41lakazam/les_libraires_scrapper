#!/usr/local/bin/python3
#
# results.py
# src
#
# Created by Eyal Shukrun on 10/12/20.
# Copyright 2020. Eyal Shukrun. All rights reserved.
#
import flask
import subprocess

app = flask.Flask(__name__)

def crawler_running():
    return open("running.state", "r").read() == "1"

@app.route('/')
def index():
    last_crawl = open("last_crawl_date.txt", 'r').read()

    if crawler_running():
        return f"""
            Run crawler <a href="/runspider">here</a>
            See results of the {last_crawl} <a href='/results'>here</a>
        """
    else:
        return f"""
            Crawler is already running.
            See results of the {last_crawl} <a href='/results'>here</a>
        """

@app.route('/runspider')
def runspider():
    if crawler_running():
        return "Impossible action, crawler is already running"

    subprocess.run(["scrapy", "runspider", "leslibraires/spiders/books_spider.py"])
    return "Crawler running"

@app.route('/results')
def result():
    return open("results.csv", 'r').read()

@app.route('/results-as-csv')
def result_as_csv():
    try:
        return flask.send_file("results.csv")
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
