# Rummage

Product searcher for MTG stores in South Africa. The following stores are supported:

- Luckshack
- Dracoti
- Top Deck
- Sad Robot
- The Warren
- A.I. Fest
- Battle Wizards
- D20 Battleground
- The Stone Dragon

Previously supported:

- HQ Gaming - The store is no longer operating.
- Underworld Connections

## Issues

The following stores need to be updated to handle "no stock" better. Currently they retrieve items that are out of stock:

- The Warren
- Sad Robot

The following stores have very "vague" matching when finding results:

- Battle Wizards

The following stores have issues finding the correct prices to display for stock that is available:

- Top Deck

## Development

Setup a Python virtual environment first. Then run the following commands from within that environment.

Install the necessary python packages:

```sh
pip install -r src/requirements.txt
```

Add a `.env` file to the project root. Use the `.example.env` file as a template.

Next, spin up a docker container for the `postgres` database only:

```sh
docker-compose --env-file .env -f docker-compose.yml -f docker-compose.dev.yml up -d postgres
```

Run the migrations on the new database:

```sh
python ./src/manage.py migrate
```

Load the store fixtures:

```sh
python ./src/manage.py loaddata stores.json
```

Collect the static files:

```sh
python ./src/manage.py collectstatic
```

Finally, run the django server for testing:

```sh
python ./src/manage.py runserver
```

The django server will be served on: http://localhost:8000

## Production

This project can be run in production using docker.

Ensure that you always run docker commands as a non-root user who is part of the `docker` group.

Also, before beginning update the `.env` file to contain production appropriate values (including unique passwords). Also, remove the following values from the env file:

1. `SKIP_TASK_QUEUE`
2. `DEBUG`.

To build and run the docker containers, enter the following command:

```sh
docker-compose --env-file .env -f docker-compose.yml -f docker-compose.prod.yml up -d --no-deps --build
```

This will spin up all the full suie of docker containers. **Make sure that you are not using the dev docker-compose file**. The postgres database will be exposed on a public port if you use the dev configuration. The only thing preventing public access to it will be your postgres password and firewall (if configured).

You can then migrate the database:

```sh
docker exec rummage_web_1 /bin/sh -c "python manage.py migrate"
```

Load the store fixtures:

```sh
docker exec rummage_web_1 /bin/sh -c "python manage.py loaddata stores.json"
```

Collect the static files:

```sh
docker exec rummage_web_1 /bin/sh -c "python manage.py collectstatic --no-input"
```
