from bs4 import BeautifulSoup

# Открываем и читаем HTML файл
with open('Локации.htm', 'r', encoding='utf-8') as file:
    content = file.read()

# Инициализируем BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Находим нужный div
container = soup.find('div', class_='t951__grid-cont js-store-grid-cont t-store__grid-cont_col-width_stretch t-container_100 t-store__grid-cont_mobile-grid t-store__mobile-two-columns mobile-two-columns t951__container_mobile-grid')

# Извлекаем все ссылки
links = [a['href'] for a in container.find_all('a', href=True)]

with open('links.txt', "w") as f:
    for link in links:
        f.write(link+'\n')