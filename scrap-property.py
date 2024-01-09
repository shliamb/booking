# Берем ссылки из scrap-object и парсим отдельно каждую

import requests
#import json
import re
#import time
from bs4 import BeautifulSoup

url = "https://www.booking.com/hotel/id/villa-kira.html?aid=304142&label=gen173nr-1FCAQoggJCC3JlZ2lvbl80MTI3SDFYBGhoiAEBmAExuAEZyAEM2AEB6AEB-AEDiAIBqAIDuAKmgO-sBsACAdICJDRkYjc0MDJlLWE1ZjEtNGM4NC05ZTQ4LWUwMzZlOTYzNThiNtgCBeACAQ&sid=c6ca475addcf36c97acb90be3c5f14f3&all_sr_blocks=981244801_370400883_6_0_0;checkin=2024-01-10;checkout=2024-01-13;dest_id=900048236;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=9;highlighted_blocks=981244801_370400883_6_0_0;hpos=9;matching_block_id=981244801_370400883_6_0_0;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=981244801_370400883_6_0_0__725400000;srepoch=1704795641;srpvid=4dfa370c037e00e3;type=total;ucfs=1&#hotelTmpl"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
}

clear_url = url[:-10] # Очищенный url

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print(f"\n status: {response.status_code}\n")
hotel_results = []

# object.name
for el in soup.find_all("div", {"role": "main"}):
    object_name_element = el.find("h2", {"class": "pp-header__title"})
    if object_name_element is not None:
        object_name = object_name_element.text.strip()
        hotel_results.append({"object.name": object_name})

# Интерактивная карта объекта откроется если к его URL добавить #map_opened-hotel_sidebar_static_map
# object.location (Ссылка на геолокацию)
object_location = clear_url + "#map_opened-hotel_sidebar_static_map"  
hotel_results.append({"object.location": object_location})

# property.name   
for el in soup.find_all("tr", {"class": "js-rt-block-row"}):
    room_type_element = el.find("span", {"class": "hprt-roomtype-icon-link"})
    if room_type_element is not None:
        room_type = room_type_element.text.strip()
        hotel_results.append({"property.name ": room_type})
# Пояснение: производится поиск по всем tr, если они не содержат искомое, то выдает Null, проверяем и отсееваем.

# property.data_room_id
for el in soup.find_all("a", {"class": "hprt-roomtype-link"}):
    data_room_id = el.get("data-room-id")
    if data_room_id is not None:
        hotel_results.append({"data-room-id": data_room_id})
# data-room-id="data_room_id" возможно это и есть id room

# property.url
for el in soup.find_all("a", {"class": "hprt-roomtype-link"}):
    property_url = el.get("href")
    if property_url is not None:
        property_url = clear_url + property_url
        hotel_results.append({"property.url": property_url})
# Раскомментировать property_url - будет формироваться ссылка, очень длинная

#property.square  
for el in soup.find_all("div", {"data-component": "hotel/new-rooms-table/highlighted-facilities"}):
    room_square_element = el.find("div", {"data-name-en": "room size"})
    if room_square_element is not None:
        room_square = room_square_element.text.strip()
        hotel_results.append({"property.square": room_square})

# property.view.garden
for el in soup.find_all("div", {"data-component": "hotel/new-rooms-table/highlighted-facilities"}):
    garden_element = el.find("svg", {"class": "bk-icon -streamline-garden"})
    garden = garden_element is not None
    hotel_results.append({"property.view.garden": garden})
# Так как нет явного значения garden, в каждой строке таблицы ищу иконку garden, нашел - ок, помечаю.

#property.view.swiming_pool 
for el in soup.find_all("div", {"data-component": "hotel/new-rooms-table/highlighted-facilities"}):
    room_pool_element = el.find("svg", {"class": "bk-icon -streamline-pool"})
    room_pool = room_pool_element is not None
    hotel_results.append({"property.view.swiming_pool": room_pool})

#property.view.balcony
for el in soup.find_all("div", {"data-component": "hotel/new-rooms-table/highlighted-facilities"}):
    room_balcony_element = el.find("svg", {"class": "bk-icon -streamline-resort"})
    room_balcony = room_balcony_element is not None
    hotel_results.append({"property.view.balcony": room_balcony})

#property.price.new
for el in soup.find_all("tr", {"class": "js-rt-block-row"}):
    price_element_new = el.find("div", {"class": "bui-price-display__value"})
    if price_element_new is not None:
        price_text = price_element_new.text.strip()
        price_digits_new = re.sub(r'\D', '', price_text)  # Удаляем все, кроме цифр
        hotel_results.append({"property.price.new": price_digits_new})

#property.price.old
for el in soup.find_all("tr", {"class": "js-rt-block-row"}):
    price_element = el.find("div", {"class": "js-strikethrough-price"})
    if price_element is not None:
        price_text = price_element.text.strip()
        price_digits = re.sub(r'\D', '', price_text)  # Удаляем все, кроме цифр
        hotel_results.append({"property.price.old": price_digits})

# property.Breakfast
for el in soup.find_all("div", {"class": "hprt-block"}):
    breakfast = el.find("div", {"class": "bui-list__description"})
    if breakfast is not None:
        property_breakfast = breakfast.text.strip()
        hotel_results.append({"property.Breakfast": property_breakfast})

# property.bed
for el in soup.find_all("div", {"class": "hprt-roomtype-bed"}):
    bed = el.find("li", {"class": "rt-bed-type"})
    if bed is not None:
        property_bed = bed.text.strip()
        hotel_results.append({"property.bed": property_bed})

for li in soup.find_all("li", class_="bedroom_bed_type"):
    # Получаем текст из элемента <strong> и <span>
    bedroom_number = li.find("strong").get_text(strip=True).replace(u"\xa0", u" ")
    bed_type = li.find("span").get_text(strip=True)
    if bed_type is not None:
        # Комбинируем данные в одну строку
        bedroom_info = f"{bedroom_number} {bed_type}"
        hotel_results.append({"property.rooms.count": bedroom_info})

for res in hotel_results:
    print(res)

#json_data = json.dumps(hotel_results, ensure_ascii=False, indent=4) # Временно, так визуально понятнее

#print(json_data)
    
# object.name
# for el in soup.find_all("div", {"role": "main"}):
#     hotel_results.append({
#     "object.name": el.find("h2", {"class": "pp-header__title"}).text.strip(),
#     #"link": el.find("a", {"id": "hotel_address"}),
#     #"location": el.find("span", {"data-testid": "address"}).text.strip(),
#     #"pricing": el.find("span", {"data-testid": "price-and-discounted-price"}).text.strip()[3::],
#     #"rating": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[0],
#     #"review_count": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[1],
#     #"thumbnail": el.find("img", {"data-testid": "image"})['src'],
# })