# discourse-data

## Instructions for setup on linux

- Version of ChromeDriver used: 92.0.4515.107
- [Download ChromeDriver](https://chromedriver.chromium.org/downloads) 
- Extract and copy the extracted folder into `/usr/local/bin`.
- Create a virtual environment
- Make sure you have `virtualenv` and `pipenv` installed. 
```
virtualenv env
```
- Activate the environment
```
source env/bin/activate
```
- Install Requirements
```
pipenv install
```

<br>

## Command to crawl the data from your choice of website

- Suppose the key of the defined website is 2 . Then in the command-line , use this command
```
python discourse.py site-2
```
- A new json file with name as defined in configuration will be generated.

- If site-{id} is not provided, by default [BoingBoing](https://bbs.boingboing.net) will be crawled.

<br>

## How to manipulate this repository according to your convenience

> Open the discourse.py file.

> 3 websites are added currently. But you may add more if required.

> Define any new discourse websites with integer keys inside "configurations" in the predefined format.

> Change your category wishlist as per your convenience after going through the website manually

<br>

## Extra Actions for Convenience:

> You may use them in any order and in all possible combinations

- Debug: See what is actually happening using the ChromeDriver
```
python discourse.py site-2 -d
python discourse.py site-2 --debug
```

- Limit Number of Posts for each topic
```
python discourse.py site-2 max_posts=5
```

- Limit Number of Topics for each category in wishlist
```
python discourse.py site-2 max_topics=3
```

## Try out the Single Topic Crawler

- Change the baseurl of the topic inside the main namespace.
- Choose a suitable max limit of posts to crawl.
- Change debug to False if you don't want to see the automated browser actions.
- Run the following command:
```
python discourse_topic_crawler.py
```
- Sit back and relax. A new file "topic_wise_test.json" will be generated.
