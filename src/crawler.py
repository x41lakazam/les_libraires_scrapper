#!/usr/local/bin/python3
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from leslibraires.spiders.books_spider import BooksListSpider
import logging

import flask
import multiprocessing


class SpiderProcess:

    def __init__(self):
        self.crawler = None
        self.process = None
        self.end_event = multiprocessing.Event()
        self.beginning_event = multiprocessing.Event()
        self.refresh_process()

    def start(self):
        if not self.is_running():
            self.refresh_process()
            return self.process.start()

    def get_pid(self):
        return self.process.pid

    def is_running(self):
        if not self.beginning_event.is_set():
            print("YO")
            return False
        if self.end_event.is_set():
            self.onclose()
            return False
        return True

    def refresh_process(self):
        self.crawler = CrawlerProcess()
        self.crawler.crawl(BooksListSpider)


        f = self.get_function_with_event(self.crawler.crawl, self.beginning_event, self.end_event)
        self.process = multiprocessing.Process(target=f, name="crawler", daemon=True)

    def onclose(self):
        self.process.join()
        self.refresh_process()

    @staticmethod
    def get_function_with_event(f, start_event, end_event):
        def newf(*args, **kwargs):
            start_event.set()
            end_event.clear()
            r = f(*args, **kwargs)
            start_event.clear()
            end_event.set()
            return r
        return newf




app = flask.Flask(__name__)
spider_process = SpiderProcess()


@app.route('/')
def index():

    return """
        <html>
        <body>
            <a href="/run-crawler">Run crawler</a>
        </body>
        </html>
    """

@app.route('/run-crawler')
def run_crawler():
    if spider_process.is_running():
        return "The crawler is still running"
    else:
        spider_process.start()


        return """
            Crawler running, check his state <a href="/crawler-state">here</a>
        """

@app.route('/crawler-state')
def crawler_state():
    if spider_process.is_running():
        return "The crawler is still running"
    else:
        return """
            The crawler finished, find the result <a href="/result">here</a>
        """

@app.route('/result')
def result():
    if spider_process.is_running():
        return "The crawler is still running"
    else:
        return open("results.csv", 'r').read()

@app.route('/crawler-kill')
def crawler_kill():
    spider_process.process.kill()
    return "OK"



if __name__ == "__main__":
    app.run(debug=True, port=5001)

