import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
}

URL = 'https://www.propertiesguru.com/residential-search/2,3,4bhk-residential-for-sale-in-new_delhi/'
# URL = 'https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi'

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

total_prop = int(soup.select('span.numberofproperty')[0].text)
print('============================= Total  properties:',total_prop,' =============================')

page_count = 0

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

while page_count <= total_prop :
	
	if page_count==0:
		# url = 'https://www.propertiesguru.com/residential-search/2,3,4bhk-residential-for-sale-in-new_delhi/'
		url = 'https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi'
	else:
		# url = "https://www.propertiesguru.com/search?viewtype=list&cityid=1081&propertytype=sell&reffid=1&minbudget=0&maxbudget=0&bedroom=2,3,4&type=ajax&mobile=y&slimit=%d"%(page_count)
		url = "https://www.propertiesguru.com/search?viewtype=list&propertytype=sell&cityid=1081&reffid=1&cat=3,28,29,30&bedroom=2&type=ajax&slimit=%d"%(page_count)
	print('Currently accessing: ',url)
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	frame = soup.find_all('div', class_='filter-property-list detailurl')
	frame_len = len(frame)

	for i in range(frame_len):
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
	
	page_count += 10

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

df = pd.DataFrame({'Category':category,'Location':location,'Cost':cost,'Rate':rate,'Area':area,'Facing':facing,'Status':status,'Floor':floor,'Furnishing':furnishing,'Ownership':ownership,'Bathroom':bathroom,'Owner_name':owner_name}) 
df.to_csv('property_details.csv', index=False, encoding='utf-8')
print('============================= csv saved at',os.getcwd(),' =============================')