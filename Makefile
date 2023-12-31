.PHONY: install
install:
	poetry install

.PHONY: run-server
run-server:
	poetry run python -m core.manage runserver

.PHONY: migrate
migrate:
	poetry run python -m core.manage makemigrations
	poetry run python -m core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations



.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: update
update: install migrate;

.PHONE: shell
shell:
	poetry run python -m core.manage shell


.PHONY: odds
odds:
	poetry run python -m core.manage odds_api

.PHONY: scrape
scrape:
	poetry run python -m core.manage run_scrapers


m ?= "lazy commit"

lazy-git:
	git add .
	git commit -m "$(m)"
	git push


collectstatic:
	source venv/bin/activate
	poetry run python3 -m core.manage collectstatic --noinput

