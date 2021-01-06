# **newscastAPI**

<p align="center">
  <img src="./assets/title.png" style="width:800px;height:500px">
</p>

**newscastAPI** is a simple REST API to get you all the news articles for any given query word.

The API provides headlines, source of the articles, published timestamps, urls and various other useful data which potentially has numerous practical use cases such as tracking sentiment of a specific person in news, searching for buzz words and so on.

> **NOTE:** This is an early release of the API, hence certain features are still under development.

You can search news articles using the following options:

- **Keywords:** You can search for any news articles which contains the keyword (using exact match).
- **timeperiod** You can specify the time period that you want articles to be published on. For example, search for `trump` from `03-01-2021` to `06-01-2021`. There is also an additional option of choosing how many articles to be returned for each day for any given keyword with in a timeperiod.

Other options and features are still under development.

## **Goal of the project:**

Even though there are a lot of other APIs that provide the same serive, almost all of them are paid and expensive, so I just thought of developing it on my own and turned out to be an exciting project.

## **Usage:**

**API:** `https://newscast-api.herokuapp.com/api`

```python
# Python 3.7.9

import requests

# by default, returns the 10 recent news headlines in the database
url = "https://newscast-api.herokuapp.com/api"

response = requests.get(url)
result = response.json()["results"]

# results is a list of dict
print(*result, sep="\n")
```

```js
// node.js
const fetch = require("node-fetch");

fetch("https://newscast-api.herokuapp.com/api", {
  method: "GET",
})
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    console.log("Request succeeded with JSON response", data);
  })
  .catch(function (error) {
    console.log("Request failed", error);
  });
```

## **Architecture**

newscastAPI consists of 2 components,

1. Data collection Pipeline
2. Data serving pipeline

The following are describes the flow of operation in each of the pipeline.

<p align="center">
  <img src="./assets/data.png">
</p>

## **Concurrent Speed Test**

## **To-Do List**

**Publication**

- [ ] Get a logo
- [x] Usage: example scripts
- [ ] Architecture design of the API
- [ ] LinkedIn post

**Development**

- [ ] Complete the timeperiod query method
- [ ] Test the speed of the API - Benchmark the speed

**To be Implemented**

- [ ] Implementing caching using redis
- [ ] Top keywords that occurs in news for anygiven day
