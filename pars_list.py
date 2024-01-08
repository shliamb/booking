import csv
import requests

#
url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
querystring = {
    "dest_id": "900048236",
    "search_type": "CITY",
    "arrival_date": "2024-01-08",
    "departure_date": "2024-01-09",
    "adults": "1",
    "children_age": "0",
    "room_qty": "1",
    "page_number": "5",
    "languagecode": "en-us",
    "currency_code": "IDR"
}

headers = {
    "X-RapidAPI-Key": "eaba7d2b81msh649ec9f780fc116p100e26jsn446abee67f91",
    "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Обработка данных и запись в CSV
with open('hotels.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Заголовки для CSV файла
    writer.writerow(['Hotel_id', ''])

    # Перебор данных и запись в CSV
    for item in data['data']['hotels']:  # Используй 'data' и 'hotels'
        hotel_id = item['hotel_id']
        writer.writerow([hotel_id])

print("Данные сохранены в hotels.csv")





