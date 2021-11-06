<h2 align="center" style="font-weight:bold;">NewscastAPI</h2>

<p align="center">
  <a style="padding: 0 10px;" target="#" href="#inspiration">Inspiration</a> • 
  <a style="padding: 0 10px;" target="#" href="#releases">Releases</a> • 
  <a style="padding: 0 10px;" href="#contributing">Contributing</a> 
</p>

**NewscastAPI** is a web service to provide news for a given word from various sources.

The API provides the following data for each news article,

1. Headline
2. Source
3. url to the article
4. published timestamp
5. category
6. country

**Applications:** Tracking sentiment of a specific person in news, searching for buzz words, etc.

<h3 style="font-weight:bold;" id="inspiration">Inspiration</h3>

I was working on a personal project to track sentiment of a given word across news articles and tweets hence I wanted an API to fetch all the news headlines a given word.

Luckily, I found quite a lot of alternatives which provided the exact service, but all of them were either expensive or had a lot of restrictions for its usage.  So I thought of building something which does the job at an acceptable performance.

<h3 style="font-weight:bold;" id="releases">Releases</h3>

* 0.1.0
  * ADD: Google news crawler, Endpoint to access news.  

<h3 style="font-weight:bold;" id="contributing">Contributing</h3>

When contributing to this repository, please first 
discuss the change you wish to make via issue or email.

1. Implement crawlers for new sites