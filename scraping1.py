import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
}

URL = 'https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi'

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(URL)
time.sleep(1)



# //ul[@class='property-type room-no pull-right']/li[.=3]
elem = driver.find_element_by_tag_name("body")

no_of_pagedowns = 20

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1
time.sleep(10)



def get_data():
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    total_prop = int(soup.select('span.numberofproperty')[0].text)
    print('============================= Total  properties:',total_prop,' =============================')

    category=[]
    location=[]
    cost=[]
    rate=[]
    area=[]
    facing=[]
    status=[]
    floor=[]
    furnishing=[]
    ownership=[]
    bathroom=[]
    owner_name=[]

    frame = soup.find_all('div', class_='filter-property-list detailurl')
    frame_len = len(frame)
    for i in range(total_prop):
        name,loc = soup.find_all('h1',class_='filter-pro-heading')[i].get_text().split('  ')
        # print('category:',name,'||','location:',loc)
        category.append(name)
        location.append(loc)

        price= soup.find_all('div',class_='property-price')[i].get_text().split()
        # print('cost:',price[1],'|| rate:',price[2])
        cost.append(price[1])
        rate.append(price[2])

        details= soup.find_all('div',class_='row filter-pro-details')[i].get_text().split()
        # print('area:',details[0][4:],'|| facing:',details[3][6:],' || status:',' '.join(details[4:])[6:])
        area.append(details[0][4:])
        facing.append(details[3][6:])
        status.append(' '.join(details[4:])[6:])

        attrs = soup.find_all('ul',class_='pro-list')[i].get_text().split('\n')
        # print('floor:',attrs[1],' || furnished:',attrs[2],' || ownership:',attrs[3],' || bathroom:',attrs[4][0])
        floor.append(attrs[1])
        furnishing.append(attrs[2])
        ownership.append(attrs[3])
        bathroom.append(attrs[4][0])

        ag= soup.find_all('span',class_='owner-name')[i].get_text().split()
        # print('owner-name:',' '.join(ag))
        owner_name.append(' '.join(ag))

    print('============================= Info extracted =============================')
    # print(category)
    # print(location)
    # print(cost)
    # print(rate)
    # print(area)
    # print(facing)
    # print(status)
    # print(floor)
    # print(furnishing)
    # print(ownership)
    # print(bathroom)
    # print(owner_name)
    return {'Category':category,'Location':location,'Cost':cost,'Rate':rate,'Area':area,'Facing':facing,'Status':status,'Floor':floor,'Furnishing':furnishing,'Ownership':ownership,'Bathroom':bathroom,'Owner_name':owner_name}

data = get_data()
# print(data) 

df = pd.DataFrame(data) 
df.to_csv('property_details.csv', index=False, encoding='utf-8')
print('============================= csv saved at',os.getcwd(),' =============================')



'''
driver.refresh();

driver.find_element_by_css_selector('li.nav-item.dropdown.bedroomdropdown').click()
driver.find_elements_by_xpath('//ul[@class=\'property-type room-no pull-right\']/li[.=3]')[0].click()
driver.find_elements_by_xpath('//ul[@class=\'property-type room-no pull-right\']/li[.=4]')[0].click()

time.sleep(3)
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(3)

elem = driver.find_element_by_tag_name("body")
no_of_pagedowns = 20

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1
time.sleep(15)

data1 = get_data()
# print(data) 

df = pd.DataFrame(data1) 
df.to_csv('property_details_3-4-bhk.csv', index=False, encoding='utf-8')
print('============================= csv saved at',os.getcwd(),' =============================')
'''