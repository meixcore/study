import requests

url = "https://dog.ceo/api/breeds/image/random"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    print("Случайная картинка собаки:")
    print(data["message"])
else:
    print(f"Ошибка запроса: {response.status_code}")

url2 = "https://dogapi.dog/api/v2/facts"

response2 = requests.get(url2)

if response2.status_code == 200:
    data = response2.json()

    print("Факты о собаках:")

    for fact in data["data"]:
        print("-", fact["attributes"]["body"])
else:
    print(f"Ошибка запроса: {response2.status_code}")