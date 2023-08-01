CC=docker-compose

build:
	$(CC) build

run: build
	$(CC) up -d

stop:
	$(CC) down

status:
	@$(CC) ps -a --status running --services |xargs echo Running:

test-module:
	$(CC) run worker /usr/local/bin/pytest modules/tests/metrics.py

create-admin:
	$(CC) run app /usr/local/bin/python utils/create_user.py