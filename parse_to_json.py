import os
import pandas as pd
import json

def transliterate(text):
    """
    Транслитерация текста с русского на английский.
    """
    translit_map = {
        " ": "-",
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ё": "yo", "ж": "zh", "з": "z", "и": "i",
        "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
        "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch",
        "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya",
        "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D",
        "Е": "E", "Ё": "Yo", "Ж": "Zh", "З": "Z", "И": "I",
        "Й": "Y", "К": "K", "Л": "L", "М": "M", "Н": "N",
        "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T",
        "У": "U", "Ф": "F", "Х": "Kh", "Ц": "Ts", "Ч": "Ch",
        "Ш": "Sh", "Щ": "Shch", "Ъ": "", "Ы": "Y", "Ь": "",
        "Э": "E", "Ю": "Yu", "Я": "Ya",
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '0': '0'
    }
    return ''.join(translit_map.get(char, '') for char in text)

def parse_excel_to_json(file_path, output_json_path, photo_column, fields_to_include, exclude_empty=True):
    data = pd.read_excel(file_path)
    
    if fields_to_include:
        data = data[fields_to_include]
    
    if exclude_empty:
        data = data.dropna(how='all')
    
    data_json = data.to_dict(orient='records')
    locationsSubTypes = ['Усадьбы, памятники архитектуры', 'Мосты', 'Поля и карьеры', 'Аэропорт', 'Спортивные сооружения', 'Канатная дорога', 'Промышленные зоны', 'Храмы и монастыри', 'Нижний Новгород', 'Достопримечательность', 'Заброшенные и недостроенные объекты', 'Набережные', 'Городские площади, улицы', 'Парки', 'Вокзалы', 'Учреждения культуры', 'Зеленые «уголки»', 'Арт-объекты', '']
    for record in data_json:
        direct = record[photo_column]
        photos = []
        for photo in os.listdir(direct):
            photos.append(f'public/{direct}/{photo}')
        record[photo_column] = photos
    for record in data_json:
        if type(record['Название']).__name__ != 'str':
            record['Название'] = 'null'
        record['Название'] = " ".join(record['Название'].split())
        record['name'] = record['Название']
        del record['Название']

        if type(record['Описание']).__name__ != 'str':
            record['Описание'] = 'null'
        record['description'] = record['Описание']
        del record['Описание']

        if type(record['Адрес']).__name__ != 'str':
            record['Адрес'] = 'null'
        record['address'] = record['Адрес']
        del record['Адрес']

        record['photoGallery'] = record['Фото']
        del record['Фото']

        record['translitName'] = transliterate(record['name'])
        record['city'] = {"id": 652}
        record['locationsTypes'] = {"id": 1}
        if type(record['Тип локации']).__name__ != 'str':
            record['Тип локации'] = ''
        record['locationsSubTypes'] = {"id": locationsSubTypes.index(record['Тип локации']) + 1}
        del record['Тип локации']

    # Сохранение JSON в файл
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)


# Настройки
file_path = "Локации.xlsx"
output_json_path = "output.json"
photo_column = "Фото"
fields_to_include = ["Название", "Описание", "Адрес", "Фото", 'Тип локации']

parse_excel_to_json(file_path, output_json_path, photo_column, fields_to_include)
