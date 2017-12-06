from collections import defaultdict
from flask import Flask, request, redirect, jsonify
from github import Github

import dateutil.parser
import logging
import os
import sys
import threading
import urllib.request

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

github = Github(os.environ["GITHUB_TOKEN"])

projects = ("ambassador", "forge", "telepresence", "kubernaut", "scout", "scout.py", "work-tracker")

projections = {
    "work-tracker": "kuberscout",
    "scout.py": "kuberscout",
    "scout": "kuberscout",
    "kubernaut": "kuberscout",
    "ambassador": "ambassador",
    "forge": "forge",
    "telepresence": "telepresence"
}

changelogs = {
    "forge": "https://raw.githubusercontent.com/datawire/forge/master/docs/docs/reference/changelog.md",
    "telepresence": "https://raw.githubusercontent.com/datawire/telepresence/master/docs/reference/changelog.md",
    "ambassador": "https://raw.githubusercontent.com/datawire/ambassador/master/CHANGELOG.md"
}

issues = []


def histogram():
    return defaultdict(lambda: defaultdict(lambda: []))


def week(date):
    if date:
        return dateutil.parser.parse(date).isocalendar()[1]
    else:
        return None


def sync():
    issues = []

    for project in projects:
        repo = github.get_repo("datawire/{}".format(project))

        repo_issues = []
        for issue in repo.get_issues(state="all"):
            issue_dict = {
                'repo_url': repo.url,
                'project': repo.full_name,
                'created_at': issue.created_at,
                'closed_at': issue.closed_at,
                'pull_request': issue.pull_request is not None
            }

            repo_issues.append(issue_dict)

        issues.extend(repo_issues)
    return issues


def releases():
    for project, changelog in changelogs.items():
        url = urllib.request.urlopen(changelog)
        data = url.read().decode("utf-8")

        for line in data.splitlines():
            line = line.strip()
            parts = line.split()
            if project in ("telepresence", "forge") and parts and parts[0] == "####":
                yield project, " ".join(parts[2:]), parts[1]
            elif parts and parts[0] == "##":
                yield project, " ".join(parts[2:]), parts[1]


def query():
    created_hist = histogram()
    closed_hist = histogram()

    for issue in issues[:]:
        if issue['pull_request']:
            continue

        project = issue['project']
        created_week = issue['created_at'].isocalendar()[1]
        created_hist[project][created_week].append(issue)

        if issue['closed_at'] is not None:
            closed_week = issue['closed_at'].isocalendar()[1]
            closed_hist[project][closed_week].append(issue)

    release_hist = histogram()
    for project, date, version in releases():
        release_hist[project][dateutil.parser.parse(date, fuzzy=True).isocalendar()[1]].append(version)

    end = "2017-11-28"
    now = dateutil.parser.parse(end).isocalendar()[1]

    result = {
        'created': created_hist,
        'closed': closed_hist,
        'releases': release_hist
    }

    return result

issues = []

class Syncer(threading.Thread):

    def run(self):
        global issues
        while True:
            issues = sync()
            time.sleep(3600)


@app.before_first_request
def download_json_web_key_set():
    Syncer().start()


@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK", 200


@app.route("/", methods=["GET"])
def get_stats():
    return jsonify(query())
