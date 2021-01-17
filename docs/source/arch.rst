Architecture
===============

This section covers the architecture of the backend of the API in detail. The entire application consists of two key components.

1. Data Collection
2. Data Serving

Data Collection Pipeline
-------------------------
.. image:: _static/collection.png

The data collection pipeline crawls news articles every 1 hour and preprocesses the data. 
The preprocessing includes datetime standardization, hashing title and country (used to for checking duplicates), creating a unix timestamp for each article.

It is hosted as a seperate container in heroku and the crawl process is managed by a cron job. Due to memory limitation for the free dyno, the crawler only crawls 
from three countries, also a lot of memory management had to be done to make it run under the allocated memory.

Data Serving Collection
-------------------------
.. image:: _static/serve.png

The data serving pipeline serves as the endpoint for the users which performs the query to the database. It is hosted as a seperate instance in heroku and to avoid the service from 
idealizing, a external service is used to ping the endpoint every 30 minutes. 

