import os
from PIL import Image

def compress_images(input_dir: str, output_dir: str, quality: int = 85):
    """
    Сжимает изображения с расширением .jpg в указанной директории, 
    создавая идентичную структуру в выходной директории.

    :param input_dir: Путь к директории с исходными изображениями.
    :param output_dir: Путь к директории для сохранения сжатых изображений.
    :param quality: Качество сжатия (от 1 до 95). 85 — стандартное качество.
    """
    for root, dirs, files in os.walk(input_dir):
        # Вычисляем путь для выходной директории
        relative_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)

        # Создаем директорию в выходной папке
        os.makedirs(output_subdir, exist_ok=True)

        for file_name in files:
            if file_name.lower().endswith('.jpg'):
                input_path = os.path.join(root, file_name)
                output_path = os.path.join(output_subdir, file_name)

                try:
                    # Сжимаем изображение и сохраняем
                    with Image.open(input_path) as img:
                        img = img.convert("RGB")  # Убедимся, что формат корректен
                        img.save(output_path, "JPEG", quality=quality)
                        print(f"Сжато: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Ошибка обработки файла {input_path}: {e}")

# Пример использования
input_directory = "img"  # Исходная директория
output_directory = "compressed_img"  # Директория для сохранения

compress_images(input_directory, output_directory, quality=75)