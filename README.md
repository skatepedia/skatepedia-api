# Skatepedia [WORK in PROGRESS]

This project runs a REST API for skate scraped data.

Tech stack used: Django + rest framework and Scrapy.




## Installation

Requires [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)



`docker-compose build`

### API

`docker-compose up`

Go to  http://localhost:9000/api/v1/


### Crawl data

`docker-compose run service scrapy crawl <spider_name>`


### Inspect data

(Just once) Create a superuser to access Django's admin.

```
docker-compose run service bash

python manage.py createsuperuser
```

To check crawled data run the web server `docker-compose up` and visit http://localhost:9000/admin/


## Resources

### Skate Data

- https://theboardr.com/
- http://www.skatevideosite.com
- http://freestylekb.com/wiki/index.php?title=Main_Page

#### [TODO]

- [ ] Contact: http://skately.com


### Tech Resources

- [Scrapy](https://doc.scrapy.org/)
- [Django](https://docs.djangoproject.com/)
- [Xpath](https://devhints.io/xpath)
- [HEP](https://pythonhosted.org/hepcrawl/index.html)


## Project

> Note: Models don't hold relationships until scraped data is consistent.

### Components

- `skatepedia`:

Django project with an app (**api**) that exposes an API with CRUDL operations for the models defined by the **db** app.

- `scraper`:

Scrapy project that plugs `skatepedia` exporting crawled data directly into the database.


## Future [TODO]
