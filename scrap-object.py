import json
import requests
from bs4 import BeautifulSoup
import time
#from selenium import webdriver

url = "https://www.booking.com/searchresults.html?ss=Canggu&ssne=Canggu&ssne_untouched=Canggu&label=gen173nr-1FCAQoggJCC3JlZ2lvbl80MTI3SDFYBGhoiAEBmAExuAEZyAEM2AEB6AEB-AEDiAIBqAIDuAKmgO-sBsACAdICJDRkYjc0MDJlLWE1ZjEtNGM4NC05ZTQ4LWUwMzZlOTYzNThiNtgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=900048236&dest_type=city&checkin=2024-01-10&checkout=2024-01-13&group_adults=1&no_rooms=1&group_children=0"
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

# Находите элементы на странице, используя soup.find() или soup.find_all()
print(response.status_code)
hotel_results = []

for el in soup.find_all("div", {"data-testid": "property-card"}):
    hotel_results.append({
    "name": el.find("div", {"data-testid": "title"}).text.strip(),
    "link": el.find("a", {"data-testid": "title-link"})["href"],
    "location": el.find("span", {"data-testid": "address"}).text.strip(),
    "pricing": el.find("span", {"data-testid": "price-and-discounted-price"}).text.strip()[3::],
    #"rating": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[0],
    #"review_count": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[1],
    #"thumbnail": el.find("img", {"data-testid": "image"})['src'],
})

json_data = json.dumps(hotel_results, ensure_ascii=False, indent=4) # Временно, так визуально понятнее

print(json_data)

# по 25 элементов на странице, в урле первой страницы отсуствует параметр offset, что означает что первая страница
# Следующая страница содержит в конце урла offset=25 что значит что это вторая страница, добавляя по 25 можно перемещаться по страницам

# Не выходит получить прайс - null, если не указать период поиска даты, если указать, то прайс просто парситься





# driver.quit()