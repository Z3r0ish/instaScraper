# instaScraper
An Instagram Scraper made in python

# Requirements
* A *nix based OS (I'm using Arch linux)
* [Chrome / chromium based browser (I hate it too)](https://www.google.com/chrome/ "Chrome / chromium based browser (I hate it too)")
* [Chrome WebDriver (needs to match chrome version see chrome://verson)](https://sites.google.com/a/chromium.org/chromedriver/ "Chrome WebDriver (needs to match chrome version see chrome://verson)")
* [Python and pip](https://www.python.org/downloads/ "Python and pip")
* [selenium (pip install selenium)](https://pypi.org/project/selenium/ "selenium (pip install selenium)")

## How to use
1. Change line 12 to point to the location of your Chrome WebDriver (if you installed the chrome webdriver as a package just put chromedriver)
2. Put the accounts / hastags you want to scrape in the array on line 5
    * for hastags your have to put explore/tags/'your hastag'
3. Put the filepath you want to save the files on line 6
    * examples: ``/hdd/media/`` or ``/instagram/``
4. Run it by doing ``python instaScraper.py``

### [WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/ " WTFPL – Do What the Fuck You Want to Public License")