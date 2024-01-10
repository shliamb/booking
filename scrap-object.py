# Если URL не содержит offset - то это 1ая страница списка, если в конец URL - offset=25 вторая.
# Не отдает цену - null, если не указать период поиска - даты.
# В зависисмости от агента выдача разная.

#НАДО:
#фильтры протестить в url

#import json
import requests
from bs4 import BeautifulSoup
#import time
#from selenium import webdriver

url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAQoggJCC3JlZ2lvbl80MTI3SDFYBGhoiAEBmAExuAEZyAEM2AEB6AEB-AEDiAIBqAIDuAKmgO-sBsACAdICJDRkYjc0MDJlLWE1ZjEtNGM4NC05ZTQ4LWUwMzZlOTYzNThiNtgCBeACAQ&sid=c6ca475addcf36c97acb90be3c5f14f3&aid=304142&checkin=2024-01-10&checkout=2024-01-13&dest_id=900048236&dest_type=city&srpvid=88930dda9a29009b&track_hp_back_button=1&"
#page = ''
#page = '&offset=50'
#внизу пояснения
# Имитация заголовков браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


# Для JavaScript используй selenium
# driver = webdriver.Chrome()
# driver.get(url)

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print(f"\n status: {response.status_code}\n")
hotel_results = []

# object.name
for el in soup.find_all("div", {"data-testid": "property-card"}):
    object_name_element = el.find("div", {"data-testid": "title"})
    if object_name_element is not None:
        object_name = object_name_element.text.strip()
        hotel_results.append({"object.name": object_name})

# object.url
for el in soup.find_all("div", {"data-testid": "property-card"}):
    object_url = el.find("a", {"data-testid": "title-link"})["href"]
    if object_url is not None:
        hotel_results.append({"object.url": object_url})

# object.location - city
for el in soup.find_all("div", {"data-testid": "property-card"}):
    location = el.find("span", {"data-testid": "address"})
    if location is not None:
        object_location = location.text.strip()
        hotel_results.append({"object.location":  object_location})

# property.type
for el in soup.find_all("div", {"data-testid": "property-card"}):
    prop_type = el.find("h4", {"role": "link"})
    if prop_type is not None:
        property_type = prop_type.text.strip()
        hotel_results.append({"property.type": property_type})
   

for res in hotel_results:
    print(res)

#json_data = json.dumps(hotel_results, ensure_ascii=False, indent=4) # Временно, так визуально понятнее
#print(json_data)
# driver.quit()
    
# for el in soup.find_all("div", {"data-testid": "property-card"}):
#     hotel_results.append({
#     "object.name": el.find("div", {"data-testid": "title"}).text.strip(),
#     "object.url": el.find("a", {"data-testid": "title-link"})["href"],
#     "object.location.not.url": el.find("span", {"data-testid": "address"}).text.strip(),
#     "pricing": el.find("span", {"data-testid": "price-and-discounted-price"}).text.strip()[3::],

    #"rating": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[0],
    #"review_count": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[1],
    #"thumbnail": el.find("img", {"data-testid": "image"})['src'],
# })