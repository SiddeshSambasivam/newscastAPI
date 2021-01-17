Usage
===============

This is section contains a detailed doumentation of the usage and Parameters of the API. It also highlights the key aspects to be noted during its usage.

**Important Things to be Noted:**

* All the datetime is standardised to UTC time. So all the queries with date and time should be converted before hand.
* The datetime object should be in the following format: `dd/mm/yyyy, hh:mm:ss` and it is 24-hour format.
* There is always a latency of 1 hour in the news feed because of the news crawler.
* Heroku's free dyno switches off the server once its been idle for a while and has a restriction on duration of uptime for the server.

API
-----

**Endpoint:** https://newscast-api.herokuapp.com/api

By default, the API provides today's news from US, India (IN), and Singapore (SG). It fetches a curated list of news based on the set of queries provided by the end user. A query is the value that been given by the user to the API's default parameters. The following are the list of parameters,

* **query**

* **from_date**

* **to_date**

* **articles_per_day**

The News is divided in two main ways. First, the news are divided by the country in which it is published and second, by the category to which the news belongs. 

In the current release, there are three countries:

* US

* Singapore (SG)

* India (IN)

and there six different categories:

* Business

* Technology

* Entertainment

* Sports

* Science 

* Health


Parameters
-----------


Examples
-----------