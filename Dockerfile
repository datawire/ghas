FROM python:3.6-alpine
MAINTAINER Datawire <dev@datawire.io>
LABEL PROJECT_REPO_URL         = "git@github.com:datawire/argonath.git" \
      PROJECT_REPO_BROWSER_URL = "https://github.com/datawire/argonath" \
      DESCRIPTION              = "Datawire Oauth Auth0 Integration (Ambassador Extauth)" \
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
    "oauth_auth0.app:app" \
    ]
