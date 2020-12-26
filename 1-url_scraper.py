

import time
import requests
import random
import json

from urllib3.exceptions import MaxRetryError
from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


#browser = webdriver.Firefox()#Chrome('./chromedriver.exe')
PATIENCE_TIME = 60
BRANDS = ['nike','jordan','adidas','other']

#return type list per brand
def get_types(brand):
    #account for unique identifiers
    if brand == 'jordan':
        brand = 'retro-jordans'
    elif brand == 'other':
        brand = 'other-sneakers'
    type_list = []
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://stockx.com/{}".format(brand))
    time.sleep(15)
    while True:
        try:
            #if load more button present, click!
            loadMoreButton = driver.find_element_by_xpath("//div[@class='subcategory show-more']")
            print(loadMoreButton)
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(5)
        #else -> continue
        except Exception as e:
            print (e)
            break
    #capture type divs
    elems = driver.find_elements_by_xpath("//div[@class='subcategoryList']/div[@class='form-group']/div[@class='checkbox subcategory']")
    for elem in elems:
        #time.sleep(15)
        item = elem.find_element_by_tag_name('label').get_attribute('innerHTML')
        #account for unique identifiers
        if len(item.split(' ')) > 0:
            item = '-'.join(item.split(' '))
        if item == 'Other':
            item = 'footwear'
        if item.isdigit():
            item = 'air-jordan-'+item
        type_list.append(item.lower())
    driver.quit()
    print (type_list)
    return type_list

def page_information():
    brand_dict = {}
    missing = []
    sneaker_counter = 0
    years = ['before-2001','2001','2002','2003','2004','2005','2006','2007','2008','2009',
             '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    #iterate through brand & types ex. AirForce, Lebron, etc. 
    for b in BRANDS:
        type_dict = {}
        for t in get_types(b):
            page_dict = {}
            for y in years:
                #account for unique identifier
                if b == 'jordan':
                    b = 'retro-jordans'
                print ("Starting "+t.capitalize()+" "+y)
                #open URL with webdriver
                #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
                #headers = {'User-Agent': user_agent}
                #options = Options()
                #options.add_argument("user-agent=headers")
                driver = webdriver.Chrome(ChromeDriverManager().install())
                url    = "https://stockx.com/{}/{}".format(b,t)+"?years="+y
                result = True
                time.sleep(5)
                driver.get(url)
                try:
                    no_result = driver.find_element_by_xpath(".//div[@class='no-results']")
                    check     = no_result.get_attribute("innerHTML").split(' ')[0]
                    if check == "NOTHING":
                        print ('No results found. Going to next page.')
                        driver.quit()
                        continue
                except NoSuchElementException as e:
                    result = True
                    print (e)
                if result:
                    #while True, Search for presence of loading button
                    page_counter = 0
                    while True:
                        if driver.find_elements_by_class_name('css-1y02vv5 epmhwwg0') != []:
                            #wait for presence of load more button
                            #print(driver.find_elements_by_class_name('css-1y02vv5 epmhwwg0'))
                            #WebDriverWait(driver, 30).until(driver.find_elements_by_class_name('css-1y02vv5 epmhwwg0'))
                            #EC.text_to_be_present_in_element((By.XPATH, "//button[@class='btn btn-default']"), "Load More"))
                            print ("Found more pages!")
                            page_list = driver.find_elements_by_class_name('css-1y02vv5 epmhwwg0')
                            #loadMoreButton = driver.find_element_by_xpath("//button[@class='btn btn-default']")
                            for page in page_list:
                                print ("Clicking...")
                                page.click()
                                driver.implicitly_wait(5)
                                print ("Beginning Extraction")
                                #capture divs loaded from fully loaded page
                                #need to click on other pages
                                elems = driver.find_elements_by_xpath("//div[@class='browse-grid']/div[@class='tile browse-tile updated']/div[@class='tile css-1bonzt1 e1yt6rrx0']")
                                for elem in elems:
                                    #search divs for name,href,src
                                    driver.implicitly_wait(5)
                                    sneaker_counter+=1
                                    page_counter+=1
                                    #contains parent div
                                    try:
                                        href      = elem.find_element_by_tag_name('a').get_attribute("href")
                                        #search for //div/img
                                        img_tag   = elem.find_element_by_xpath(".//div[@class='css-1c5ij41 euld1y70']").get_attribute("innerHTML")
                                        #extract img_src and name
                                        img       = img_tag.split('"')
                                        print(img)
                                        name, src = img[7], img[17]
                                        print (name)
                                        #write to dict
                                        data = {
                                            "src": src,
                                            "href": href
                                            }
                                        page_dict[name] = data
                                        #exit driver
                                        time.sleep(1/(random.randint(1,100)*10000))
                                    #if scraper encounters an error, the count will be zero
                                    #identify what page is missing
                                        if page_counter == 0:
                                            missing.append([[b,t,y]])
                                    except MaxRetryError:
                                        print("found a missing link")
                                        missing.append('missing: ')
                                        missing.append([b,t,y])
                                    driver.quit()
                                    print ('Total Count: '+str(sneaker_counter))
                                    #print(page_dict)
                        else:
                        #except Exception as e:
                            print ("Only 1 page")
                            print ("Beginning Extraction")
                            elems = driver.find_elements_by_xpath("//div[@class='browse-grid']/div[@class='tile browse-tile updated']/div[@class='tile css-1bonzt1 e1yt6rrx0']")
                            print(elems)
                            print(len(elems))
                            for elem in elems:
                                #search divs for name,href,src
                                driver.implicitly_wait(5)
                                page_counter+=1
                                #contains parent div
                                try:
                                    href      = elem.find_element_by_tag_name('a').get_attribute("href")
                                #search for //div/img
                                    img_tag   = elem.find_element_by_xpath(".//div[@class='css-1c5ij41 euld1y70']").get_attribute("innerHTML")
                                #extract img_src and name
                                    img       = img_tag.split('"')
                                    #print(len(img))
                                    #print(img)
                                    name, src = img[7], img[17]
                                    print (name)
                                #write to dict
                                    data = {
                                        "src": src,
                                        "href": href
                                        }
                                    page_dict[name] = data
                                    print(page_dict)
                                    #exit driver
                                    time.sleep(1/(random.randint(1,100)*10000))
                                    #if scraper encounters an error, the count will be zero
                                    #identify what page is missing
                                    sneaker_counter+=1
                                    if page_counter == 0:
                                        missing.append([[b,t,y]])
                                except MaxRetryError:
                                        print("found a missing link")
                                        missing.append('missing: ')
                                        missing.append([b,t,y])
                                driver.implicitly_wait(10)
                                driver.quit()
                                print ('Total Count: '+str(sneaker_counter))
                                #print(page_dict)
                            
                    
            #seed page_dict[name] into type_dict
            type_dict[t] = page_dict
            print ("SEEDING TYPE...")
        #seed type_dict into total
        brand_dict[b] = type_dict
        print ("SEEDING BRANDS...")
        with open('total.json', 'w') as outfile:  
            json.dump(brand_dict, outfile, indent=4)
    #return final dictionary
    #with open('total.json', 'w') as outfile:  
        #json.dump(brand_dict, outfile, indent=4)
    with open('missing.json', 'w') as outfile:  
        json.dump(missing, outfile, indent=4)
    print ("Complete.")
    print (missing)

if __name__ == "__main__":
    page_information()