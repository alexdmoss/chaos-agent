FROM python:3.7.6-alpine3.11 AS requirements
ADD . /app
WORKDIR /app
RUN pip install pipenv=='2018.11.26'
RUN pipenv lock -r > requirements.txt
RUN pipenv lock --dev -r > requirements-dev.txt

FROM python:3.7.6-alpine3.11 AS runtime-pips
COPY --from=requirements /app /app
WORKDIR /app
RUN pip install -r requirements.txt --no-use-pep517

FROM python:3.7.6-alpine3.11 AS pytest
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
RUN pip install -r requirements-dev.txt
RUN /usr/local/bin/pytest -v --cov-report=term-missing --cov=.

FROM python:3.7.6-alpine3.11
COPY --from=runtime-pips /app/main.py /app/
COPY --from=runtime-pips /app/ascii.txt /app/
COPY --from=runtime-pips /app/chaos_agent /app/chaos_agent
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/python", "-u", "/app/main.py"]