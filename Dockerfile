# Main image for running things in a Django/Python environment.
#
# Usage:
#    docker-compose run django gunicorn --bind 0.0.0.0:8080 projectname.wsgi:application
#    docker-compose run django ./manage.py migrate
#    docker-compose run django ./manage.py shell_plus
#    docker-compose run django ./manage.py ...

# Debian-based image is faster than alpine because it can install pip wheels
# Downgraded to 3.7 https://github.com/python/typed_ast/issues/124 
# ref1: https://github.com/python/mypy/issues/7001
# ref2: https://github.com/dbader/pytest-mypy/pull/44
FROM python:3.7-buster

# Configuration defaults
ENV SUITEDCONNECTORS_ROOT "/opt/suitedconnectors.poker"
ENV DATA_DIR "$SUITEDCONNECTORS_ROOT/data"
ENV HTTP_PORT "8000"
ENV DJANGO_USER "www-data"
ENV VENV_NAME ".venv-docker"

# Setup system environment variables neded for python to run smoothly
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# Install system requirements
RUN apt-get update && apt-get install -y \
    # psycopg2 requirements
    python-psycopg2 libpq-dev \
    # fish shell
    fish \
    # npm
    npm \
    # gosu
    gosu \
    # Needed for typed-ast dependency
    build-essential \
    # python requirements
    python3-dev python3-pip python3-venv jq \
    # supervisor
    supervisor && \
    # cleanup apt caches to keep image small
    rm -rf /var/lib/apt/lists/*

# Setup Python virtualenv separately from code dir in /opt/suitedconnectors/.venv-docker.
#   It needs to be outside of the code dir because the code is mounted as a volume
#   and would overwite the docker-specific venv with the incompatible host venv.

WORKDIR "$SUITEDCONNECTORS_ROOT"
RUN pip install virtualenv && \
    virtualenv "$VENV_NAME"
ENV PATH="$SUITEDCONNECTORS_ROOT/$VENV_NAME/bin:${SUITEDCONNECTORS_ROOT}/bin:./node_modules/.bin:${PATH}"

# Add .git HEAD to container 
ADD .git/HEAD ./.git/HEAD
ADD .git/refs/heads/ ./.git/refs/heads/

# Install the python dependencies from requirements.txt into /opt/suitedconnectors.poker/.venv-docker.
COPY ./core/Pipfile.lock "$SUITEDCONNECTORS_ROOT/Pipfile.lock"
RUN jq -r '.default,.develop | to_entries[] | .key + .value.version' "$SUITEDCONNECTORS_ROOT/Pipfile.lock" | \
    pip install --no-cache-dir -r /dev/stdin && \
    rm "$SUITEDCONNECTORS_ROOT/Pipfile.lock"
RUN npm install --global npm yarn
RUN userdel "$DJANGO_USER" && addgroup --system "$DJANGO_USER" && \
    adduser --system --ingroup "$DJANGO_USER" --shell /bin/false "$DJANGO_USER"

# Workers require to write data and own the directory
RUN mkdir "$SUITEDCONNECTORS_ROOT/data"
RUN mkdir "$SUITEDCONNECTORS_ROOT/data/logs"
RUN mkdir -p "$SUITEDCONNECTORS_ROOT/core/js/node_modules"
RUN chown "$DJANGO_USER"."$DJANGO_USER" "$SUITEDCONNECTORS_ROOT/data"
RUN chown -R "$DJANGO_USER"."$DJANGO_USER" "$SUITEDCONNECTORS_ROOT/data/logs"
RUN chown -R "$DJANGO_USER"."$DJANGO_USER" "$SUITEDCONNECTORS_ROOT/core"

ENTRYPOINT [ "/opt/suitedconnectors.poker/bin/entrypoint.sh" ]
