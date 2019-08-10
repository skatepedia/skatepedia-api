# Skatepedia [WORK in PROGRESS]

A REST API for skate scraped data.


## Installation

This project runs an API with acces to the scrapped data. (Django + rest framework + Scrapy)

`python3 -m venv ~/.virtualenvs/skatepedia-api/`

`source ~/.virtualenvs/skatepedia-api/bin/activate`

`pip install -r requirements-dev.txt`


Run in local:


`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`


## Crawl data

`scrapy crawl <spider_name>`



## Data Resources

- http://skately.com/
- https://theboardr.com/
- http://www.skatevideosite.com/skatevideos
- http://freestylekb.com/wiki/index.php?title=Main_Page


## Tech Resources

- https://devhints.io/xpath
- https://docs.djangoproject.com/
- https://doc.scrapy.org/
