import re
import os
from loguru import logger
import requests
import zipfile
from urllib.parse import urlparse
from datetime import datetime


class Tool:
    """
    Вспомогательные статические методы для AI-агента
    """

    # Константы
    C_FS_TEMP_FOLDER = "temp"                                       # Папка для временных файлов
    C_FS_DELIM = "/"                                                # Разделитель в файловой системе          

    @staticmethod
    @logger.catch
    def extract_code(is_text: str) -> str:
        """
        Извлечь код из текста, содержащего маркеры начала и конца кода

        Args:
            is_text (str): текст ответа от LLM

        Returns:
            str: исходный код
        """
        # значение по умолчанию
        rs_result = None
        
        # анализируем
        ls_full = is_text
        la_text = ls_full.split("```")
        if len(la_text) > 0:
            # нашли - берем 1й фрагмент и удаляем название языка
            rs_result = la_text[1].replace("python\n", "")
        
        # возвращаем результат
        return rs_result

    @staticmethod
    @logger.catch
    def get_temp_folder() -> str|None:
        """
        Сгенерировать путь к новой временной папке

        Returns:
            str|None: результат (по умолчанию - None)
        """
        # Значение по умолчанию
        rs_result = None

        # Генерируем уникальное имя для папки
        lo_now = datetime.now()
        ls_ts = lo_now.strftime("%Y%m%d_%H%M%S")
        rs_result = Tool.C_FS_TEMP_FOLDER + Tool.C_FS_DELIM + ls_ts
        
        # Возвращаем путь к папке
        return rs_result

    @staticmethod
    @logger.catch
    def download_github_repo(is_url: str) -> str|None:
        """
        Скачать GitHub-репозиторий во временную папку

        Args:
            is_url (str): URL репозитория

        Returns:
            str|None: путь к временной папке с содержимым репозитория (по умолчанию - None)
        """
        # Значение по умолчанию
        rs_result = None

        # Извлекаем имя пользователя и репозитория из URL
        path_parts = urlparse(is_url).path.strip('/').split('/')
        username, repo_name = path_parts[0], path_parts[1]
        
        # Формируем URL для скачивания ZIP-архива
        zip_url = f"https://github.com/{username}/{repo_name}/archive/refs/heads/master.zip"         # main -> master
        
        # Создаем корневую временную папку в проекте, если она не существует
        os.makedirs(Tool.C_FS_TEMP_FOLDER, exist_ok=True)

        # Создаем папку c уникальным именем
        ls_folder = Tool.get_temp_folder()
        os.makedirs(ls_folder, exist_ok=True)
        rs_result = ls_folder
        
        # Скачиваем ZIP-архив
        response = requests.get(zip_url, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        # Сохраняем и распаковываем архив
        zip_path = os.path.join(ls_folder, f"{repo_name}.zip")
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ls_folder)
        
        # Удаляем ZIP-архив
        os.remove(zip_path)
        
        # Возвращаем путь к папке
        return rs_result

    @staticmethod
    @logger.catch
    def get_all_files(is_folder: str) -> list|None:
        """
        Получить список всех файлов в папке (включая подпапки)

        Args:
            is_folder (str): путь к папке

        Returns:
            list|None: список файлов (по умолчанию - None)
        """
        return [os.path.join(root, name)
            for root, dirs, files in os.walk(is_folder)
            for name in files]

    @staticmethod
    @logger.catch
    def get_file_extension(is_file: str) -> str:
        """
        Получить расширение файла

        Args:
            is_file (str): имя файла

        Returns:
            str: расширение файла
        """
        return os.path.splitext(is_file)[1]

if __name__ == "__main__":
    # Пример использования
    repo_url = "https://github.com/nyatsun/calc_and_win"
    Tool.download_github_repo(repo_url)
