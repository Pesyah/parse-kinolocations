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
    for record in data_json:
        direct = record[photo_column]
        photos = []
        for photo in os.listdir(direct):
            photos.append(f'public/{direct}/{photo}')
        record['avatar'] = photos[0]
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
        record['locationsTypes'] = [{"id": 1}, {"id": 2}]
        if 'портивные' in record['Группа локации']:
            print(record['name'])
        if 'рхитектур' in record['Группа локации']:
            record['locationsSubTypes'] = {"id": 13}
        elif 'Природные' in record['Группа локации']:
            record['locationsSubTypes'] = {"id": 15}
        elif 'Зеленые' in record['Группа локации']:
            record['locationsSubTypes'] = {"id": 15}
        elif 'Заброшенные' in record['Группа локации']:
            record['locationsSubTypes'] = {"id": 14}
        elif 'Учреждения культуры' in record['Группа локации']:
            record['locationsSubTypes'] = {"id": 17}
        elif 'ородской' in record['Группа локации']:
            record['locationsSubTypes'] = {"id": 18}
        else:
            record['locationsSubTypes'] = {"id": 20}
        del record['Группа локации']

        if 'русчатка' in record['Дорожное покрытие']:
            record['locationsRoadSurface'] = {"id": 3}
        elif 'сфальт' in record['Дорожное покрытие']:
            record['locationsRoadSurface'] = {"id": 1}
        else:
            record['locationsRoadSurface'] = {"id": 4}
        del record['Дорожное покрытие']

        record['locationsRequiredPermissions'] = record['Требует разрешений']
        if 'Да' in record['Требует разрешений']:
            record['locationsRequiredPermissions'] = {"id": 2}
        else:
            record['locationsRequiredPermissions'] = {"id": 1}
        del record['Требует разрешений']

        if cities.count(record['Город']) == 0:
            record['city'] = { "id": 68 }
        else:
            record['city'] = { "id": cities.index(record['Город']) + 1}
        del record['Город']
        if 'открыт' in record['Доступность'] or 'Открыт' in record['Доступность']:
            record['locationsAccessibility'] = {"id": 1}
        else:
            record['locationsAccessibility'] = {"id": 3}
        del record['Доступность']

        record['coords'] =              record['Координаты']
        record['locationFeatures'] =    record['Особенности']
        if record['Работа с дронами'] == 'Требуется разрешения вблизи населенного пункта'\
            or record['Работа с дронами'].strip() == 'Требуется разрешение':
            record['dronesType'] = { "id": 3 }
        else:
            record['dronesType'] = { "id": 1 }
        del record['Работа с дронами']

        record['locationsRestrictions'] = {"id": 5}
        record['locationsBackgroundLandscape'] = {"id": 11}
        record['locationsTrees'] = {"id": 6}
        record['locationsSunriseView'] = {"id": 5}
        record['locationsTransportAvailability'] = [{"id": 8}]
        record['locationsParking'] = {"id": 6}


        record['status'] = {"id": 4}


        record['workingHours'] =        record['Часы работы']
        record['buildingsNearby'] =     record['Здания поблизости']
        record['additionalFeatures'] =  record['Дополнительные возможности']

        del record['Координаты']
        del record['Особенности']
        del record['Ограничения']
        del record['Часы работы']
        del record['Здания поблизости']
        del record['Дополнительные возможности']
        del record['Тип локации']

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
