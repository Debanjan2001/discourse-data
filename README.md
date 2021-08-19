# discourse-data

> Version of ChromeDriver used: 92.0.4515.107

<br>

>[Download ChromeDriver](https://chromedriver.chromium.org/downloads) 

<br>

> How to use this repository according to your convenience

>> Open the discourse.py file.

>> Three websites are added.

>> Define any new discourse websites with integer keys inside object "configurations" in the same way as the predefines ones.

>> Change your category wishlist as per your convenience after going through the website manually

<br>

> Commands to crawl the data from your choice of website and other options

- Suppose the key of the defined website is 2 . Then in the command-line , use this command
```
python discourse.py site-2
```

> If you want to see what's going on in the background => Run the file in debug mode using any one of the following command:
```
python discourse.py site-2 --debug
python discourse.py site-2 -d
```