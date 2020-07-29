from selenium import webdriver
import urllib.request
import discord
from discord.ext import commands
from config import *
import time
import json

# log into the client
client = discord.Client()

#
# functions to parse the json file, I'm not going to comment all of them
#

def getPrefix(client, message):
    with open(jsonPath, 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def getPath():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['path']

def getScrollTime():
    with open(jsonPath, 'r') as f:
        scrollTime = json.load(f)
    return int(scrollTime['scrollTime'])

def getDriverPath():
    with open(jsonPath, 'r') as f:
        driverPath = json.load(f)
    return driverPath['driverPath']

# sets the prefix
client = commands.Bot(command_prefix=getPrefix)

# when the bot is logged in print it in the terminal
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# make the path command
@client.command()
async def path(ctx, newPath):
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    
    path[str("path")] = newPath

    with open(jsonPath, 'w') as f:
        json.dump(path, f, indent=4)
    await ctx.send('Set filepath to ' + newPath)

# make the scrollTime command
@client.command()
async def scrolltime(ctx, newScrollTime):
    with open(jsonPath, 'r') as f:
        scrollTime = json.load(f)
    
    scrollTime[str("scrollTime")] = int(newScrollTime)

    with open(jsonPath, 'w') as f:
        json.dump(scrollTime, f, indent=4)
    await ctx.send('Set scroll time to ' + newScrollTime)
    
# make the driverPath command
@client.command()
async def driverpath(ctx, newDriverPath):
    with open(jsonPath, 'r') as f:
        driverPath = json.load(f)
    
    driverPath[str("driverPath")] = newDriverPath

    with open(jsonPath, 'w') as f:
        json.dump(driverPath, f, indent=4)
    await ctx.send('The driver path has been set to ' + newDriverPath)

# make the scrape command
@client.command()
async def scrape(ctx, *args):
    # send in the chat the accounts that will be scraped
    if len(args) > 1:
        await ctx.send('{} accounts to scrape: {}'.format(len(args), ', '.join(args)))
    elif len(args) == 1:
        await ctx.send('{} account to scrape: {}'.format(len(args), ', '.join(args)))
    elif len(args) < 1:
        await ctx.send('Not engough accounts')
        return

    i = 0
    numberPost = 0
    null = 0

    # set the arguments to the accounts
    accounts = args

    # sets the options for chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')

    # opens chrome
    driver = webdriver.Chrome(executable_path=getDriverPath(),   chrome_options=options)

    try:
        for acc in accounts:
            account = (accounts[i].replace("#", "explore/tags/"))

            # loads in the account page and scrolls down
            driver.get('https://www.instagram.com/' + account + '/')

            # gets the follower count
            try:
                followers = driver.find_element_by_xpath(followerXpath).text
                print(account + " has " + followers)
                await ctx.send(account + " has " + followers + " followers")
            except:
                followers = 'null'
                print("wasn't able to get followers")
                await ctx.send("wasn't able to get followers")

            # scrolling (does a max of 4 page heights)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            scroll=0
            while(match==False):
                lastCount = lenOfPage
                time.sleep(getScrollTime())
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
                if scroll > 4:
                    match=True
                scroll += 1

            # gets all post
            posts = []
            links = driver.find_elements_by_tag_name('a')
            for link in links:
                p = 0
                post = link.get_attribute('href')
                if '/p/' in post:
                    posts.append(post)
                    p += 1
                    print(post)

            # spliting up the url, finding out if it's an image or video and downloading it
            download_url = ' '
            for post in posts:
                driver.get(post) # loads in the post
                shortcode = driver.current_url.split('/')[-2] # gets the url code

                # get the time it was created
                datetime = driver.find_element_by_xpath(timeXpath).get_attribute('datetime')
                print(datetime)
                
                # find out if it's a video or immage
                type = driver.find_element_by_xpath(connentXpath).get_attribute('content')
                print(type)
                # create file name
                name = [getPath(), accounts[i], '&', followers, '&', datetime]
                nameJoined = ''.join(name)
                
                # gets the numbers of likes
                try:
                    likes = driver.find_element_by_xpath(likesXpath).text
                    print(likes)
                    likesSplit = likes.split(' ')
                # if it couldn't get the likes
                except:
                    likesSplit = ['null', 'null'] 
                    print('Could not get the likes')
                    null += 1

                # downloads it
                if type == 'instapp:photo':
                    download_url = driver.find_element_by_xpath('//meta[@property="og:image"]').get_attribute('content')
                    urllib.request.urlretrieve(download_url, nameJoined + '&' + likesSplit[0] + '&' + "{}.jpg".format(shortcode))
                else:
                    download_url = driver.find_element_by_xpath('//meta[@property="og:video"]').get_attribute('content')
                    urllib.request.urlretrieve(download_url, nameJoined + '&' + likesSplit[0] + '&' + "{}.mp4".format(shortcode))
            print(type + ' ' + download_url)
            numberPost += 1
            i += 1

        print('instaScraper has finished')
        print(str(numberPost) + ' post where scraped')
        print(str(null) + ' have no likes')

        # makes the embed
        embed=discord.Embed(title="instaScraper has finished")
        embed.add_field(name="Accounts", value=' '.join(accounts), inline=False)
        embed.add_field(name="Scraped post", value=str(numberPost), inline=True)
        embed.add_field(name="Post with no likes", value=str(null), inline=True)
        
        # sends the embed
        await ctx.send(embed=embed)

    except:
        # sends a msg if it fails
        await ctx.send('There was a problem while trying to scrape post')
        print('There was a problem while trying to run the script')
    
    finally:
        driver.quit()

# immport the token
client.run(token)