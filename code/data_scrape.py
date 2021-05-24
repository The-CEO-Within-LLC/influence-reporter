from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from selenium import webdriver
import re as re


driver_location = '' #loaction of geckodriver
options = Options()
options.headless = True #makes selenium run in headless modes (no window).

def data_grab_facebook_business(url):
    '''

    :param url: facebook business link. has form: https://business.facebook.com/*/?business_id=*
    :return: returns the title and the larger of follows and likes as a tuple (likes or follows, title)
    '''
    try:
        uClient = uReq(url)
        page_soup = soup(uClient.read(), "html.parser")  # stores page data
        uClient.close()
        info_list = page_soup.find_all("div", {"class": "_4bl9"})  # index 1 and 2. 1=like, 2=follow
        likes_result = re.search( "div>(.*) people like",str(info_list[1])) #gets the html line that stores the likes and grabs the value between"div>" and " people like"
        likes=int(likes_result.group(1).replace(",","")) #group(1) stores the string we grabbed in the previous line, turns it into an int
        follows_result= re.search( "div>(.*) people follow",str(info_list[2])) #gets the html line that stores the follows and grabs the value between"div>" and " people follow"
        follows = int(follows_result.group(1).replace(",",""))
        title = re.search( ".com/(.*)/?business",str(url)).group(1) #gets the portion of the url that contains it's title
        return (max(follows, likes), title)
    except:
        print(str(url) + ' is inaccessible')
        return (0,re.search( ".com/(.*)/?business",str(url)).group(1))

def data_grab_facebook(url):
    '''

    :param url: facebook page link. has form: https://www.facebook.com/*/
    :return: returns the title and the larger of follows and likes as a tuple (likes or follows, title)
    '''
    try:
        uClient = uReq(url)
        page_soup = soup(uClient.read(), "html.parser")  # stores page data
        uClient.close()
        info_list = page_soup.findAll("div", {"class": "_4bl9"})  # index 1 and 2. 1=like, 2=follow
        likes_result = re.search("div>(.*) people like", str(info_list[1]))  # gets the html line that stores the likes and grabs the value between"div>" and " people like"
        likes = int(likes_result.group(1).replace(",",""))  # group(1) stores the string we grabbed in the previous line, turns it into an int
        follows_result = re.search("div>(.*) people follow", str(info_list[2]))  # gets the html line that stores the follows and grabs the value between"div>" and " people follow"
        follows = int(follows_result.group(1).replace(",",""))
        print(likes)
        title = re.search("com/(.*)", str(url)).group(1)  # gets the portion of the url that contains it's title
        return (max(likes, follows), title)
    except:
        print(str(url) + ' is inaccessible')
        return (0, re.search("com/(.*)", str(url)).group(1))

def data_grab_waldenu(list):
    '''

    :param list: a list of scholarworks urls. The form is less general so here are two examples:  https://scholarworks.waldenu.edu/jsbhs/vol12/iss1/7/ https://scholarworks.waldenu.edu/dissertations/9938/
    :return: the number of reads and the title of the paper as a tuple (reads, title)
    '''
    try:
        driver = webdriver.Firefox(executable_path=driver_location,options=options)  
        tuple_list = []
        for url in list:
            driver.get(url)
            html = driver.page_source
            print(html)
            page_soup = soup(html, "html.parser")  # stores page data
            infobox = page_soup.find("span", {"id": "article-downloads"})
            downloads = int(re.search(">(.*)</span>", str(infobox)).group(1).replace(",", ""))
            title_source = page_soup.find("div", {"id": "title"})
            title = re.search('">(.*)</a></p>', str(title_source)).group(1)
            tuple_list.append((downloads, title))
        driver.close()
        return tuple_list
    except:
        print('scholarworks items inaccessible')
        null_list=[(0,'error')]
        return null_list

def data_grab_researchgate(url): 
    '''

    :param url: a url which leads to a researchgate profile
    :return: the number of impressions over all researchgate material published by the profile user
    '''
    try:
        title = 'researchgate profile'
        driver = webdriver.Firefox(executable_path=driver_location,options=options)
        driver.get(url)
        html = driver.page_source
        driver.close()
        page_soup = soup(html, "html.parser")  # stores page data
        reads = page_soup.findAll("div", {"nova-e-text nova-e-text--size-xl nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit"})
        reads_int = int(re.search('color-inherit">(.*)</div>', str(reads[1])).group(1).replace(',', ''))
        return ((reads_int, title))
    except:
        print('researchgate inaccessible')
        return (0, 'researchgate profile')




