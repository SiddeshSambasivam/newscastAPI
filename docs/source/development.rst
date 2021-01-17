Contributing to Newscast API
=======================================

There are many ways to contribute to Newscast API. The following are a list of some of them:

* Use Newscast API in your projects and blog about them to increase its visibility.
* Report any potential bugs or request new features in the API by opening an issue in the `official repository <https://github.com/SiddeshSambasivam/newscastAPI>`_.
* Improve the documentation. See the following sub-section for more details
* Writing new spiders in scrapy for news sites

Improve Documentation
^^^^^^^^^^^^^^^^^^^^^^
1. **Doc strings:** Improving the doc strings for every function in the `app.py` file for better understanding of the function.
2. **Examples:** Write more examples on how to use the API.
3. **Official documentation:** Improve the official documentation by adding additional information, correcting grammatical errors, etc.

Write Spiders for new news sites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`scrapy` Library was used to develop the spiders which crawls and scrapes content from news sites. 
Therefore, you could develop new spiders for a specific site and add it inside the `develop` folder.

    1. Fork the `git repository <https://github.com/SiddeshSambasivam/newscastAPI>`_
    2. Create a new branch `git checkout -b develop`
    3. Work on the `develop` folder if you are creating a new spider. 


Features under Development
---------------------------

1. When there is no result found for a given query in the database, search for the news online and return the results (also update the database). 
2. Query by category 
3. Query by country
4. Caching