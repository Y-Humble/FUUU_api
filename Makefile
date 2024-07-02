dc = docker compose
local_dc_file = docker-compose-dev.yaml
env_prod = ./src/.env.dev

.PHONY: local-up
local-up:
	$(dc) -f $(local_dc_file) --env-file $(env_prod) up

.PHONY: local-down
local-down:
	$(dc) -f $(local_dc_file) --env-file $(env_prod) down