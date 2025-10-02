import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = "https://habr.com/ru/articles/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

def get_articles():
    response = requests.get(URL, headers=HEADERS,verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    for article in articles:
        # Заголовок
        title_tag = article.find("h2")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        link = title_tag.find("a")["href"]

        # Дата
        date_tag = article.find("time")
        date = date_tag["datetime"].split("T")[0] if date_tag else "нет даты"

        # Текст превью
        preview_text = article.get_text(separator=" ").lower()

        # Проверка ключевых слов
        if any(word.lower() in preview_text for word in KEYWORDS):
            print(f"{date} – {title} – {link}")


if __name__ == "__main__":
    get_articles()