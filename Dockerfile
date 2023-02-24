# `python-base` sets up all our shared environment variables
FROM --platform=linux/amd64 python:3.9.5-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.2.0 \
    POETRY_HOME=/opt/poetry \
    WORKDIR_PATH=/app

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $WORKDIR_PATH

# `builder` stage is used to build deps + create our virtual environment
FROM python-base as builder
RUN : \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        netcat \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && :

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python

# copy project requirement files here to ensure they will be cached.
COPY poetry.lock pyproject.toml ./

RUN : \
    && poetry config virtualenvs.create true \
        # install in current directory
    && poetry config virtualenvs.in-project true \
    # Further, we will use the same image for testing and deployment purposes.
    && poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && :
RUN poetry run pip install -r requirements.txt

# `production` image used for runtime
FROM python-base as production
ENV PATH="$WORKDIR_PATH/.venv/bin:$PATH"
COPY entrypoint.sh $WORKDIR_PATH
COPY --from=builder $WORKDIR_PATH $WORKDIR_PATH
COPY src/ $WORKDIR_PATH
