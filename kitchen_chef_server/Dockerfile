FROM python:3.11 AS base


ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1 


RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-root $(test "$DEPLOYMENT_ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . .
COPY ./patches/rdflib_sqarql.py  /usr/local/lib/python3.11/site-packages/rdflib/plugins/sparql/evaluate.py
COPY ./patches/rdflib_parser.py  /usr/local/lib/python3.11/site-packages/rdflib/plugins/sparql/parserutils.py

COPY ./patches/rdflib_sqarql.py  ./.venv/lib/python3.11/site-packages/rdflib/plugins/sparql/evaluate.py
COPY ./patches/rdflib_parser.py  ./.venv/lib/python3.11/site-packages/rdflib/plugins/sparql/parserutils.py

EXPOSE 8000

####################
# debugger
####################

FROM base as debug

RUN poetry add debugpy

WORKDIR /app

ENTRYPOINT ["poetry", "run", "uvicorn",  "kitchen_chef_server.__main__:app", "--host", "0.0.0.0", "--reload"]

####################
# HOST
####################

FROM base as networkhost

RUN poetry add debugpy

WORKDIR /app

ENTRYPOINT ["poetry", "run", "uvicorn",  "kitchen_chef_server.__main__:app", "--reload"]

####################
# primary
####################

FROM base as primary

WORKDIR /app
ENTRYPOINT ["poetry", "run", "uvicorn",  "kitchen_chef_server.__main__:app", "--host", "0.0.0.0" ]

