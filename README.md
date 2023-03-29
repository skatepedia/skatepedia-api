# Skatepedia

> **Warning**
>
> **WORK in PROGRESS**

Uses: Django + DRF + Postgresql + Celery + IPFS + Scrapy

## Quickstart
### Installation

Requires [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)


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


## Crawling data

> **Warning**
>
> **Spiders may become outdated, as scraped websites may change or go offline**


`docker-compose run service scrapy crawl <spider_name>`

## API

[Open the openapi.yml](http://localhost:9000/api/v1/schema) specification.

or the [Swagger UI](http://localhost:9000/api/v1/schema/swagger-ui).

## Interplanetary Skate Archive [TODO]

> **Warning**
>
> **Process for publishing on IPFS is a work in progress**

`docker-compose run service python manage.py distill-local staticsite`

in the `staticsite` folder run:

`npx all-relative`

Then upload the whole staticsite folder to IPFS to have a decentralized static site.

`ipfs add -r  staticsite`

Go to https://ipfs.io/ipfs/[staticsite_folder_cid]/videos/funhouse-3.html

## Resources

### Skate Data

Huge thanks to everyone in the skateboarding community for contribuiting and collaborating.
Special thanks to

- [SkateVideoSite](http://www.skatevideosite.com)
- [The Board](https://theboardr.com/)
-  [http://skately.com](https://web.archive.org/web/20191003042112/) Using Web Archive since original site is down.

## Tech Resources

- [Django](https://docs.djangoproject.com/)
- [IPFS - InerplanetaryFileSystem](https://ipfs.tech/)
- [Celery - Distributed Task Queue](https://docs.celeryq.dev/en/stable/)
- [DRF - REST Framework](https://www.django-rest-framework.org/)
- [django-filters](https://django-filter.readthedocs.io/en/stable/index.html)
- [DRF nested routes](https://github.com/alanjds/drf-nested-routers)
- [Scrapy](https://doc.scrapy.org/)

## Development
### Troubleshooting

- `ipfs`
```
skatepedia-api-ipfs-1      | Error: serveHTTPGateway: manet.Listen(/ip4/172.19.0.3/tcp/8080) failed: listen tcp4 172.19.0.3:8080: bind: cannot assign requested address
```

The `docker-compose.yml` ipfs service overrides the default healthcheck. If the service can't bind an address:port there might be an error in the ipfs config, try deleting the `ipfs_data` folder.
