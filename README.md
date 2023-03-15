# Skatepedia


> **Warning**
>
> **WORK in PROGRESS**

This project runs a REST API for skate scraped Quickstart.

### Installation

Requires [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)


`docker-compose build`

`docker-compose up`

### Crawl data

`docker-compose run service scrapy crawl <spider_name>`

### Debug

`docker-compose run service bash`

### Configuration

All the environment configuration variables should be stored in the .env file.

## Data Resources

### Skate Data

Huge thanks to everyone in the skateboarding community for contribuiting with public data.

- https://theboardr.com/
- http://www.skatevideosite.com
- http://freestylekb.com/wiki/index.php?title=Main_Page

Need to contact: http://skately.com

## Tech Resources

- [Django](https://docs.djangoproject.com/)
- [Scrapy](https://doc.scrapy.org/)
- [Xpath](https://devhints.io/xpath)
- [HEP](https://pythonhosted.org/hepcrawl/index.html)
