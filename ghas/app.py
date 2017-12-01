from flask import Flask, request, redirect, jsonify

import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

GITHUB_USER = os.environ["GITHUB_USER"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK", 200


@app.route("/", methods=["GET"])
def get_stats():
    return "OK /", 200
