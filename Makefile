DC = docker compose
LOCAL_DC_FILE = docker-compose-dev.yaml
ENV = ./environs/.env
ENV_DEV = ./environs/.env.dev
ENV_TEST = ./environs/.env.test

.PHONY: dev-up dev-down test-up test-down

dev-up:
	sed -i 's/MODE.*/MODE=DEV/' $(ENV)
	$(DC) -f $(LOCAL_DC_FILE) --env-file $(ENV_DEV) up

dev-down:
	$(DC) -f $(LOCAL_DC_FILE) --env-file $(ENV_DEV) down

test-up:
	sed -i 's/MODE.*/MODE=TEST/' $(ENV)
	$(DC) -f $(LOCAL_DC_FILE) --env-file $(ENV_TEST) up

test-down:
	$(DC) -f $(LOCAL_DC_FILE) --env-file $(ENV_TEST) down
