from selenium import webdriver
import time
import urllib.request

accounts = ["acount1", "account2"]
filepath = "/insta/media/"
print(accounts)

i = 0

# open chrome / open 
driver = webdriver.Chrome("chromedriver")

for account in accounts:
    
    # loads in the account page and scrolls down
    driver.get('https://www.instagram.com/' + accounts[i] + '/')
    
    # gets the follower count
    followers = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span""").text
    print(followers)

    # scrolling (does a max of 4 page heights)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    scroll=0
    while(match==False):
        lastCount = lenOfPage
        time.sleep(.5)
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
        datetime = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div/article/div[3]/div[2]/a/time""").get_attribute('datetime')
        print(datetime)
        
        # find out if it's a video or immage
        type = driver.find_element_by_xpath('//meta[@property="og:type"]').get_attribute('content')

        # create file name
        name = [filepath, accounts[i], '&', followers, '&', datetime]
        nameJoined = ''.join(name)
        
        # gets the numbers of likes
        try:
            likes = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div/article/div[3]/section[2]/div/div/button""").text
            print(likes)
            likesSplit = likes.split(' ')
        # if it couldn't get the likes
        except:
            likesSplit = ['null', 'null'] 
            print('Could not get the likes')

        # downloads it
        if type == 'video':
            download_url = driver.find_element_by_xpath('//meta[@property="og:video"]').get_attribute('content')
            urllib.request.urlretrieve(download_url, nameJoined + '&' + likesSplit[0] + '&' + "{}.mp4".format(shortcode))
        else:
            download_url = driver.find_element_by_xpath('//meta[@property="og:image"]').get_attribute('content')
            urllib.request.urlretrieve(download_url, nameJoined + '&' + likesSplit[0] + '&' + "{}.jpg".format(shortcode))
        
        print(type + ' ' + download_url)
    i += 1

driver.quit()

print('instaScraper has finished')
