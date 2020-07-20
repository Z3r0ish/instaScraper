from selenium import webdriver
import time
import urllib.request

account = ["account1", "account2", "explore/tags/hashtag1", "explore/tags/hashtag2"]
filepath = ' '

i = 0

# open chrome / open 
driver = webdriver.Chrome(' ')

for a in account:
    print(account)
    driver.get('https://www.instagram.com/' + account[i] + '/')

    # scrool
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(5)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    # gets all post
    posts = []
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)
    print(posts)

    # spliting up the url, finding out if it's an image or video and downloading it
    download_url = ' '
    for post in posts:
        driver.get( post )
        shortcode = driver.current_url.split('/')[-2]
        type = driver.find_element_by_xpath('//meta[@property="og:type"]').get_attribute('content')
        if type == 'video':
            download_url = driver.find_element_by_xpath('//meta[@property="og:video"]').get_attribute('content')
            urllib.request.urlretrieve(download_url, filepath +"{}.mp4".format(shortcode))
        else:
            download_url = driver.find_element_by_xpath('//meta[@property="og:image"]').get_attribute('content')
            urllib.request.urlretrieve(download_url, filepath +"{}.jpg".format(shortcode))
        
        print(type + ' ' + download_url)
    i += 1
