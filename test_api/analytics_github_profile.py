import requests
from collections import Counter

def get_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка: не удалось получить данные. Код: {response.status_code}")
        return None

    if response.status_code == 404:
        print(f"Ошибка: не удалось получить данные. Код: {response.status_code}")
        return None

    if response.status_code == 403:
            print(f"Ошибка: превышен лимит запросов к Github API. Код: {response.status_code}")
            return None

    return response.json()

def analyze_repos(repos):
    total_repos = len(repos)

    total_stars = 0
    most_starred_repo = None

    language = []

    for repo in repos:
        stars = repo['stargazers_count']
        total_stars += stars

        if most_starred_repo is None or stars > most_starred_repo['stargazers_count']:
            most_starred_repo = repo
        
        if repo['language'] is not None:
            language.append(repo['language'])
    
    language_counter = Counter(language)

    return {
        "total_repos": total_repos,
        "total_stars": total_stars,
        "most_starred_repo": most_starred_repo,
        "languages": language_counter
    }
    

def main():
    username = input('Введите никнейм пользователя на github: ')
    
    repos = get_repos(username)
    if repos is None:
         return
    
    analytics = analyze_repos(repos)

    print(
        f"Аналитика профиля Github {username}:\n"
        "-------------------------------------\n"
        f"- Количество публичных репозиториев: {analytics['total_repos']}\n"
        f"- Общее количество звёзд: {analytics['total_stars']}"
    )

    most_starred_repo = analytics['most_starred_repo']

    if most_starred_repo:
        print(f"- Самый популярный репозиторий: {most_starred_repo['name']} (⭐ {most_starred_repo['stargazers_count']})")
    else:
        print("- Самый популярный репозиторий: нет репозиториев")
    
    print("- Топ языков программирования:")
    if analytics['languages']:
        for language, count in analytics['languages'].most_common():
            print(f" - {language}: {count} реп.")
    else:
        print('- Языки не указаны')

main()