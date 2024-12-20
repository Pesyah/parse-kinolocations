# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from bs4 import BeautifulSoup
# import time
# import os
# import requests
# import pandas as pd

# options = Options()
# options.add_argument('--headless')

# driver = webdriver.Firefox(options=options)


# urls = None
# with open('links.txt', 'r', encoding='utf-8') as f:
#     urls = f.readlines()

# data = []
# count = 0
# for url in urls:
#     title = ''
#     type_ = ''
#     description = ''
#     address = ''

#     img_folder = f"img/{count}"
#     os.makedirs(img_folder, exist_ok=True)

#     try:
#         count += 1

#         driver.get(url)

#         time.sleep(1)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')

#         # Начинаем парсить
#         title = soup.find('meta', property='og:title')['content']
#         type_ = soup.find('div', class_='t-descr').get_text(strip=True)
#         description = soup.find('div', class_='js-store-prod-text t-store__prod-popup__text t-descr t-descr_xxs').get_text(strip=True)
#         address = soup.find('div', class_='js-store-prod-text t-store__prod-popup__text t-descr t-descr_xxs').find('div').contents[-1].text
#         description = description.split(address)[0] # вырезаю адрес из всего текста

#     except Exception as e:
#         print(e)
#         print(url)

#     slider_items = soup.find('div', class_='t-slds__items-wrapper t-slds_animated-none t-slds__nocycle').select('meta[itemprop="image"]')
#     for i, meta in enumerate(slider_items, start=1): # сохраним все картинки
#         img_url = meta['content']

#         img_data = requests.get(img_url).content

#         img_filename = os.path.join(img_folder, f"image_{i}.jpg")
#         with open(img_filename, 'wb') as img_file:
#             img_file.write(img_data)

#     data.append({
#         "ID": count,
#         "Название": title,
#         "Тип локации": type_,
#         "Описание": description,
#         "Адрес": address,
#         "Фото": img_folder,
#     })

# driver.quit()

# file_path = 'Локации.xlsx'
# df = pd.read_excel(file_path)

# new_data_df = pd.DataFrame(data)
# df = pd.concat([df, new_data_df], ignore_index=True)

# with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
#     df.to_excel(writer, index=False)


distr = []

with open('districts.txt', encoding='utf-8') as f:
    distr = [x.strip('\n') for x in f.readlines()]
with open('districts_array.txt', 'w', encoding='utf-8') as f:
    f.write(str(distr))
print(distr)