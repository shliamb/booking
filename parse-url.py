from urllib.parse import urlparse, parse_qs

# Парсим обе ссылки
url1 = "https://www.booking.com/searchresults.html?ss=Canggu&ssne=Canggu&ssne_untouched=Canggu&label=gen173nr-1FCAEoggI46AdIM1gEaGiIAQGYATG4ARnIAQzYAQHoAQH4AQKIAgGoAgO4ArqM-KwGwAIB0gIkNzFhODRkZWUtNTZmYy00MGE0LTk5OTgtMjYwODZjNzVmZjEy2AIF4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=900048236&dest_type=city&checkin=2024-01-10&checkout=2024-01-13&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
url2 = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaGiIAQGYATG4ARnIAQzYAQHoAQH4AQKIAgGoAgO4ArqM-KwGwAIB0gIkNzFhODRkZWUtNTZmYy00MGE0LTk5OTgtMjYwODZjNzVmZjEy2AIF4AIB&aid=304142&ss=Canggu&ssne=Canggu&ssne_untouched=Canggu&lang=en-us&src=index&dest_id=900048236&dest_type=city&checkin=2024-01-10&checkout=2024-01-13&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&nflt=ht_id%3D203%3Bht_id%3D213"

# Разбиваем URL на компоненты
parsed_url1 = urlparse(url1)
parsed_url2 = urlparse(url2)


# Villas                            nflt=ht_id=213
# Entire homes & apartments         nflt=privacy_type=3
# Guesthouses                       nflt=ht_id=216
# Hotels                            nflt=ht_id=204

# Можно комбинировать через точку с запятой в конце URL  &nflt=ht_id=214;ht_id=204


# Получаем параметры запроса из обеих URL
query_params1 = parse_qs(parsed_url1.query)
query_params2 = parse_qs(parsed_url2.query)

# Ищем различия в параметрах
difference = {key: query_params2[key] for key in query_params2 if query_params1.get(key) != query_params2.get(key)}
print("\n")
print(difference)
