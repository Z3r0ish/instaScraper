# instaScraper
An Instagram Scraper made in python

# Requirements
* A Unix based OS (I'm using Arch linux)
* [Chrome / chromium based browser (I hate it too)](https://www.google.com/chrome/ "Chrome / chromium based browser (I hate it too)")
* [Chrome WebDriver (needs to match chrome version see chrome://verson)](https://sites.google.com/a/chromium.org/chromedriver/ "Chrome WebDriver (needs to match chrome version see chrome://verson)")
* [Python and pip](https://www.python.org/downloads/ "Python and pip")
* [Selenium (pip install selenium)](https://pypi.org/project/selenium/ "Selenium (pip install selenium)")
* [Discord.py (pip install discord.py)](https://pypi.org/project/discord.py/ "Discord.py (pip install discord.py)")
* [instaMeta](https://github.com/Z3r0ish/instaMeta/ "instaMeta")
## How to use
1. Put the discord bot token on line 1 of config.py
2. Invite the bot into your discord server
3. Change your Chrome WebDriver location by doing ``!driverpath chromedriver``(if you installed the chrome webdriver as a package just put chromedriver)
    * Of course change the prefix and chromedriver
4. Put the filepath you want to save the files to by doing ``!path /hdd/media/``
5. Change the time between scrolls (in seconds) by doing ``!scrolltime 5
`` (I found 5 seconds to be the best)
6. Run it by doing ``python instaScraper.py``

### [WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/ " WTFPL – Do What the Fuck You Want to Public License")
