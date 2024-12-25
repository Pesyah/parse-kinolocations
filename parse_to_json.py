import os
import pandas as pd
import json
from cities import cities


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
    locationsSubTypes = [
        "Достопримечательность",
        'Зеленый "уголок"',
        "Усадьбы, памятники архитектуры",
        "Спортивные сооружения",
        "Промышленные зоны",
        "Заброшенные и недостроенные объекты",
        "Городские площади, улицы",
        "Поля и карьеры",
        "Арт-объекты",
        "Усадьбы, памятники архитектуры, храмы и монастыри",
        "Вокзалы",
        "Парки",
        "Памятник",
        "Мосты",
        "Канатная дорога",
        "Аэропорт",
        "Учреждения культуры",
        "Храмы и монастыри",
        "Набережные"
    ]
    locationsSUBTYPES = {
        'Достопримечательность, зеленые "уголки"': 2,
        'Усадьбы, памятники архитектуры': 3,
        'Спортивные сооружения': 4,
        'Промышленные зоны': 5,
        'Зеленые "уголки"': 2,
        'Усадьбы, памятники архитектуры, заброшенные и недостроенные объекты': 6,
        'Зеленые «уголки»': 2,
        'Заброшенные и недостроенные объекты': 6,
        'Городские площади, улицы': 7,
        'Достопримечательность': 1,
        'Поля и карьеры': 8,
        'Арт-объекты': 9,
        'Усадьбы, памятники архитектуры, храмы и монастыри': 10,
        'Вокзалы': 11,
        'Парки': 12,
        'Памятник': 13,
        'Мосты': 14,
        'Канатная дорога': 15,
        'Аэропорт': 16,
        'Учреждения культуры': 17,
        'Храмы и монастыри': 18,
        'Набережные': 19
    }
    for record in data_json:
        direct = record[photo_column]
        photos = []
        for photo in os.listdir(direct):
            photos.append(f'public/{direct}/{photo}')
        record[photo_column] = photos
    print(list(set([x['Работа с дронами'] for x in data_json])))
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
        record['locationsTypes'] = {"id": 1}

        record['locationsSubTypes'] = {"id": locationsSUBTYPES[record['Тип локации']]}
        del record['Тип локации']
        
        if cities.count(record['Город']) == 0:
            record['city'] = { "id": 68 }
        else:
            record['city'] = { "id": cities.index(record['Город']) + 1}
        del record['Город']
        record['coords'] =              record['Координаты']
        record['availability'] =        record['Доступность']
        record['group'] =               record['Группа локации']
        record['feature'] =             record['Особенности']
        record['roadSurface'] =         record['Дорожное покрытие']
        if record['Работа с дронами'] == 'Требуется разрешения вблизи населенного пункта'\
            or record['Работа с дронами'] == 'Требуется разрешение ':
            record['dronesType'] = { "id": 3 }
        else:
            record['dronesType'] = { "id": 1 }
        record['requiresPermissions'] = record['Требует разрешений']
        record['limitation'] =          record['Ограничения']
        record['openingHours'] =        record['Часы работы']
        record['buildingsNearby'] =     record['Здания поблизости']
        record['additionalFeatures'] =  record['Дополнительные возможности']
        del record['Координаты']
        del record['Доступность']
        del record['Группа локации']
        del record['Особенности']
        del record['Дорожное покрытие']
        del record['Работа с дронами']
        del record['Требует разрешений']
        del record['Ограничения']
        del record['Часы работы']
        del record['Здания поблизости']
        del record['Дополнительные возможности']

    # Сохранение JSON в файл
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_json, json_file, ensure_ascii=False, indent=4)


# Настройки
file_path = "Локации.xlsx"
output_json_path = "output.json"
photo_column = "Фото"
fields_to_include = [
    "Название", "Описание", "Адрес", "Фото", 'Тип локации', 'Город', 'Координаты',
    'Доступность', 'Группа локации', "Особенности", 'Дорожное покрытие', 'Работа с дронами',
    'Требует разрешений', 'Ограничения', 'Часы работы', 'Здания поблизости', 'Дополнительные возможности'
]

parse_excel_to_json(file_path, output_json_path, photo_column, fields_to_include)
