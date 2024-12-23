import requests
import bs4

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Функция для проверки наличия ключевых слов в тексте
def contains_keywords(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

response = requests.get('https://habr.com/ru/articles/')
soup = bs4.BeautifulSoup(response.text, features='lxml')

articles_list = soup.select_one('div.tm-articles-list')
articles = articles_list.select('article.tm-articles-list__item')

for article in articles:
    link_tag = article.select_one('a.tm-title__link')
    if link_tag:
        link = 'https://habr.com' + link_tag['href']
        headers = link_tag.text.strip()
        time_tag = article.select_one('time')
        time = time_tag['title'] if time_tag else 'Нет даты'
        preview_text = article.select_one('div.article-formatted-body').text.strip() if article.select_one('div.article-formatted-body') else ''

        # Проверяем наличие ключевых слов в preview-информации
        if contains_keywords(headers + preview_text, KEYWORDS):
            article_response = requests.get(link)
            article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')
            full_text = article_soup.select_one('div.tm-article-body').text.strip() if article_soup.select_one('div.tm-article-body') else ''

            # Проверяем наличие ключевых слов в полном тексте статьи
            if contains_keywords(full_text, KEYWORDS):
                print(f"{time} – {headers} – {link}")
