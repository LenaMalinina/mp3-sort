import os

class FSWrapper:
    @staticmethod
    def listdir(path):
        files = os.listdir(path)
        # Проверка файла и является ли он mp3 файлом
        return [file for file in files if os.path.isfile(os.path.join(path, file)) and file.endswith('.mp3')]