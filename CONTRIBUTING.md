# Contributing

When contributing to this repository, please first discuss the change you wish to make via an issue, email, or any other method with the owners of this repository before making a change. 

Please note that we have a code of conduct. Make sure you follow it in all your interactions with the project.

## How to contribute to the project?

1. Use Newscast API in your projects and blog about them to increase its visibility.
2. Report any potential bugs or request new features in the API by opening an issue in the official repository.
3. Improve the documentation. Refer to the following sub-sections for more details:
    
    * Doc strings: Improving the doc string for any function in the app.py file for better understanding of the function.

    * [Examples](https://newscastapi.readthedocs.io/en/latest/usage.html#examples): Write more examples on how to use the API.

    * [Official documentation](https://newscastapi.readthedocs.io/en/latest/): Improve the official documentation by adding additional information, correcting grammatical errors, etc.


4. Writing new spiders in _scrapy_ for news sites:
    
    The [scrapy library](https://scrapy.org/) was used to develop the spiders which crawl and scrape content from news sites. Therefore, you could develop new spiders for a specific site and add it to the [develop directory](https://github.com/SiddeshSambasivam/newscastAPI/tree/main/develop).

      * 4.1. Fork the git repository.

      * 4.2. Create a new branch using  _git checkout -b develop_.

      * 4.3. Work in the [develop directory](https://github.com/SiddeshSambasivam/newscastAPI/tree/main/develop) if you are creating a new spider.
