import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def parse_habr_articles():
    # Загружаем главную страницу Habr с последними статьями
    response = requests.get('https://habr.com/ru/articles')
    if response.status_code != 200:
        print("Ошибка при загрузке страницы")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []  # Сюда будем собирать подходящие статьи
    
    for article_preview in soup.find_all('article'):
        title_element = article_preview.find('a', class_='tm-article-snippet__title-link')  # находим заголовок
        
        if title_element is None:
            continue
            
        title_text = title_element.text.strip()
        href = title_element['href'].strip()  # получаем ссылку на статью
        link = f"https://habr.com{href}"
        
        date_element = article_preview.find('span', class_='tm-article-snippet__datetime-published')
        published_date = date_element.time['datetime'][:10]
        
        content_preview = article_preview.find('div', class_='article-formatted-body').text.lower().strip()
        
        # Проверяем наличие ключевого слова в превью-контенте или заголовке
        found_keywords = [
            keyword for keyword in KEYWORDS 
            if keyword.lower() in content_preview or keyword.lower() in title_text.lower()
        ]
        
        if found_keywords:
            articles.append((published_date, title_text, link))
    
    return articles


if __name__ == "__main__":
    result = parse_habr_articles()
    for date, title, link in result:
        print(f"{date} – {title} – {link}")