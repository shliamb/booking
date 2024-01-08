import csv, requests, time


# Собираем данные в список, добавляя каждый раз с новой страницы с задержкой
all_data = []
for page in range(1, 3):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {
        "dest_id": "900048236",
        "search_type": "CITY",
        "arrival_date": "2024-01-08",
        "departure_date": "2024-01-09",
        "adults": "1",
        "children_age": "0",
        "room_qty": "1",
        "page_number": page,
        "languagecode": "en-us",
        "currency_code": "IDR"
    }

    headers = {
        "X-RapidAPI-Key": "eaba7d2b81msh649ec9f780fc116p100e26jsn446abee67f91",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    page_data = response.json()
    all_data.append(page_data)  # Добавляем данные со страницы в общий список
    print(f"Добавлены результаты {page} страницы \n")
    time.sleep(2)  # Задержка для API

# Из списка в словарь
hotels_data = []
for page_data in all_data:
    hotels_data.extend(page_data['data']['hotels'])

# Обработка данных и запись в CSV
with open('hotels.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Заголовки для CSV файла
    writer.writerow(['id', 'hotel_id', 'hotel_name', 'strikethroughPrice', 'grossPrice', 'currency'])

    id = 0
    # Перебор данных и запись в CSV
    for item in hotels_data:
        id = id + 1
        hotel_id = item.get('hotel_id')
        hotel_name = item['property']['name']
        strikethroughPrice = item['property']['priceBreakdown'].get('strikethroughPrice', {}).get('value')
        grossPrice = item.get('property', {}).get('priceBreakdown', {}).get('grossPrice', {}).get('value')
        currency = item['property']['currency']
        writer.writerow([id, hotel_id, hotel_name, strikethroughPrice, grossPrice, currency])

print("Данные сохранены в hotels.csv")





