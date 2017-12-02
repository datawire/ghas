FROM python:3.6-alpine
MAINTAINER Datawire <dev@datawire.io>
LABEL PROJECT_REPO_URL         = "git@github.com:datawire/ghas.git" \
      PROJECT_REPO_BROWSER_URL = "https://github.com/datawire/ghas" \
      DESCRIPTION              = "Datawire GitHub Activity Scraper GHAS" \
      VENDOR                   = "Datawire, Inc." \
      VENDOR_URL               = "https://datawire.io"

RUN apk add --no-cache \
  gcc \
  g++ \
  libffi-dev \
  make \
  python3-dev \
  openssl-dev

WORKDIR /srv

COPY requirements.txt .
RUN pip install -Ur requirements.txt

COPY . .
RUN  pip install -e .

ENTRYPOINT ["gunicorn", \
    "--access-logfile=-", \
    "--workers=3", \
    "--bind=0.0.0.0:5000", \
    "ghas.app:app" \
    ]
