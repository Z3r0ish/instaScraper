# instaScraper
An Instagram Scraper made in python

# Requirements
* A Unix based OS (I'm using Arch linux)
* [Chrome / chromium based browser (I hate it too)](https://www.google.com/chrome/ "Chrome / chromium based browser (I hate it too)")
* [Chrome WebDriver (needs to match chrome version see chrome://verson)](https://sites.google.com/a/chromium.org/chromedriver/ "Chrome WebDriver (needs to match chrome version see chrome://verson)")
* [Python and pip](https://www.python.org/downloads/ "Python and pip")
* [selenium (pip install selenium)](https://pypi.org/project/selenium/ "selenium (pip install selenium)")

## How to use
1. Put the discord bot token on line 1 of config.py
2. Change line 3 of config.py to point to the loation of your Chrome WebDriver (if you installed the chrome webdriver as a package just put chromedriver)
3. Put the filepath you want to save the files on line 3 of config.py
    * examples: ``/hdd/media/`` or ``/instagram/``
4. Change the time between scrolls (in seconds) on line 4 of config.py (I found 5 seconds to be the best)
5. Run it by doing ``python instaScraper.py``

### [WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/ " WTFPL – Do What the Fuck You Want to Public License")
