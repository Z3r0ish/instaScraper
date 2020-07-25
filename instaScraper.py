from selenium import webdriver
import time
import urllib.request
from config import *

print(accounts)

i = 0
numberPost = 0
null = 0

# open chrome / open 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(executable_path=driver,   chrome_options=options)

try:
    for account in accounts:
        
        # loads in the account page and scrolls down
        driver.get('https://www.instagram.com/' + accounts[i] + '/')
        
        # gets the follower count
        followers = driver.find_element_by_xpath(followerXpath).text
        print(followers)

        # scrolling (does a max of 4 page heights)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        scroll=0
        while(match==False):
            lastCount = lenOfPage
            time.sleep(scrollTime)
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

            # create file name
            name = [filepath, accounts[i], '&', followers, '&', datetime]
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
            if likesSplit[0] != 'null':
                if type == 'video':
                    download_url = driver.find_element_by_xpath('//meta[@property="og:video"]').get_attribute('content')
                    urllib.request.urlretrieve(download_url, nameJoined + '&' + likesSplit[0] + '&' + "{}.mp4".format(shortcode))
                else:
                    download_url = driver.find_element_by_xpath('//meta[@property="og:image"]').get_attribute('content')
                    urllib.request.urlretrieve(download_url, nameJoined + '&' + likesSplit[0] + '&' + "{}.jpg".format(shortcode))
            print(type + ' ' + download_url)
            numberPost += 1
        i += 1

    driver.quit()

    print('instaScraper has finished')
    print(str(numberPost) + ' post where scraped')
    print(str(null) + ' have no likes')

except:
    print('There was a problem while trying to run the script')