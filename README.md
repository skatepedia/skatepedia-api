# Skatepedia


> **Warning**
>
> **WORK in PROGRESS**

This project runs an skateboarding REST API.
Uses: Django + DRF + Postgresql and Scrapy

## Why ?


## Quickstart

### Installation

Running this project requirese [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)

`docker-compose build`

`docker-compose up`

The `docker-compose` file defines two services:

- database: Postgresql

- service:  django project with an API exposed in <a href="http://localhost:9000"> `http://localhost:9000`</a>

When running, migrations are checked and executed before running the wsgi server.

The `.env` file should be the main  configuration file for all the services.

### Database Configuration

For debugging purposes or to trigger django-admin commands, with both services running, open a bash session in the service container.

`docker-compose run service bash`

**Run this once**  Configure superuser for [Django's Admin Site](http://localhost:9000/admin)

`python manage createsuper user`

### Debugging and other configurations

Database introspection:

Open a `psql` :

    `docker-compose exec database psql -d skatepedia -U admin`

Open a Django shell or run any other django-admin commands.

`docker-compose run service python manage.py shell`


### Crawl data

> **Warning**
>
> **NEEDS REVIEW: many sites have changed or went offline**

`docker-compose run service scrapy crawl <spider_name>`


## Data Resources

### Skate Data

Huge thanks to everyone in the skateboarding community for contribuiting and collaborating.
Special thanks to

- [SkateVideoSite](http://www.skatevideosite.com)
- [The Board](https://theboardr.com/)

  http://skately.com (not working anymore)

## Tech Resources

- [Django](https://docs.djangoproject.com/)
- [Scrapy](https://doc.scrapy.org/)
- [Xpath](https://devhints.io/xpath)
