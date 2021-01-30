Contributing to Newscast API
=======================================

There are many ways to contribute to Newscast API. The following are a list of some of them:

* Develop new features for the API
* Improve quality of the functional components of the API
* Report any potential bugs or request new features in the API by opening an issue in the `official repository <https://github.com/SiddeshSambasivam/newscastAPI>`_.
* Improve the documentation. See the following sub-section for more details
* Use Newscast API in your projects and blog about them to increase its visibility.

How to contribute
--------------------

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Once its been discussed, proceed to fork the project and 
create a new branch with name as ``<YOUR-GITHUB-USERNAME>-Develop``.

For developmental purposes, a very small subset of the database is available in the `develop` folder. Note that the provided data if from ``16 Jan 2021 00:00:00`` till ``18 Jan 2021 23:59:59``. 

To locally deploy the API, run the following command
    
    ``python src/app.py --develop True``

This will set the API to development mode and you should be able to develop features or fix bugs locally.

Improve Documentation
^^^^^^^^^^^^^^^^^^^^^^
1. **Doc strings:** Improving the doc strings for every function in the `app.py` file for better understanding of the function.
2. **Examples:** Write more examples on how to use the API.
3. **Official documentation:** Improve the official documentation by adding additional information, correcting grammatical errors, etc.

Improving Functional Components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Use doc strings to clearly state the usage and specifications of the functions
2. Test the functions locally before pull request

Write Spiders for new news sites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`scrapy` Library was used to develop the spiders which crawls and scrapes content from news sites. 
Therefore, you could develop new spiders for a specific site and add it inside the `develop` folder.

Work on the `develop` folder if you are creating a new spider. 

