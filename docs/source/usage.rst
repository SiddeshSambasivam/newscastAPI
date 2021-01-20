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

query
^^^^^^^
    `query` parameter could be used to fetch all news articles with query in the title of the news, and by default it fetches **only** today's news. 

    * query is case insensitive and **should not** be within quotes

from_date
^^^^^^^^^^
    `from_date` parameter could be used to specify the date form which news articles is needed. When`from_date` is not specified, it starts from `dd/mm/yyyy, 00:00:00`.

to_date
^^^^^^^^^
    `to_date` parameter could be used to specify till which day you want the news articles to be published within.


Both `from_date` and `to_date` could be used to set the timeframe.

articles_per_day
^^^^^^^^^^^^^^^^^
    `articles_per_day` parameter could be used to specify how many articles should be returned for a day. By default, the the API returns 10 articles per day.


Examples
-----------

1. Empty Search

    **Sample:** `https://newscast-api.herokuapp.com/api`

    Returns today's 10 recent news.

2. Search for a query

    **Sample:** `https://newscast-api.herokuapp.com/api?query=trump`

    Returns all the news about trump in today's news.

3. Search for a query with `from_date`

    **Sample:** `https://newscast-api.herokuapp.com/api?query=covid&from_date=18/01/2021, 00:00:00`

    Returns the news about covid from 18 January, 2021 till today with 10 articles per day.

4. Search for a query with `to_date`

    **Sample:** `https://newscast-api.herokuapp.com/api?query=lebron&to_date=15/01/2021, 00:00:00`

    Returns all the news about lebron till 15 January, 2021 with 10 articles per day.

5. Search for a query with `from_date` , `to_date` and `articles_per_day`

    **Sample:** `https://newscast-api.herokuapp.com/api?query=google&from_date=15/01/2021, 00:00:00&to_date=18/01/2021, 23:59:59&articles_per_day=5`

    Returns 5 news per day from 15 Jan to 18 Jan in the year 2021 about google. 

    **Note:** The `articles_per_day` might not be very accurate and could give more or less than the specified value due to small database size.

6. Search by only timeframe

    **Sample:** `https://newscast-api.herokuapp.com/api?from_date=14/01/2021, 00:00:00&to_date=17/01/2021, 23:59:59`

    Returns all the news from 14 Jan to 17 Jan in the year 2021.