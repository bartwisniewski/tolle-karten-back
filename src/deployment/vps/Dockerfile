FROM python:3.11-slim
LABEL maintainer="bartwisniewski"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./src/deployment/vps/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/deployment/vps/scripts/ /scripts
COPY ./src/tkbproj /app/
COPY ./README.md /app/

RUN sed -i 's/\r$//' /scripts/run.sh && \
    chmod -R +x /scripts

ENV PATH="/scripts::$PATH"

CMD ["run.sh"]
