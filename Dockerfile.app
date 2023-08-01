FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY requirements.app.txt /app/requirements.txt

RUN pip install --no-cache-dir -U -r /app/requirements.txt

COPY app /app
COPY modules /app/modules