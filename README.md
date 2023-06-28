## Project Quickstart

```bash
# make sure you've installed docker: https://docs.docker.com/engine/install/
# and docker-compose: https://docs.docker.com/compose/install/
# you may also have to add your user to the docker group: https://docs.docker.com/engine/install/linux-postinstall/

git clone https://github.com/monadical-sas/suitedconnectors.poker.git
cd suitedconnectors.poker

# Add to /etc/hosts  ->   127.0.0.1    suitedconnectors.l

docker-compose run django ./manage.py migrate
docker-compose run django ./manage.py createsuperuser
docker-compose up

# Open http://suitedconnectors.l
```

## Commands

From here, you could begin to do changes in the codebase and to run these commands for developing tasks:

```bash
# For installing yarn packages
docker-compose run --rm django suitedconnectors yarn_install
# For testing
docker-compose run --rm django suitedconnectors testpy
docker-compose run --rm django suitedconnectors testjs
# For linting
docker-compose run --rm django suitedconnectors lintpy
docker-compose run --rm django suitedconnectors lintjs
# For rebuilding docker images and update the python packages
docker-compose build
```

Some useful docker-compose commands:
```bash
# Start the stack
docker-compose start
# Stop the stack
docker-compose stop
# List the services
docker-compose ps
# Init the stack
docker-compose up
# Destroy the stack (This delete the docker containers)
docker-compose down
# Build the docker images
```

