FROM python:3.12-alpine3.20

COPY ./requirements.txt /tmp/requirements.txt
COPY . /Lonca-Project
WORKDIR /Lonca-Project

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp

ENV PATH="/py/bin:$PATH"

CMD ["python", "main.py"]