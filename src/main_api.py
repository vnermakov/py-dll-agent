# системные библиотеки
from loguru import logger                                           # pip install loguru
from fastapi import HTTPException                                   # pip install fastapi
import uvicorn                                                      # pip install uvicorn
from tqdm import trange                                             # pip install tqdm
# библиотеки проекта
from const import GC_LOG_FILE, C_TYPE_AGENT
from config import Config
from tool import Tool
from agent import AiAgent

def run_init(io_app) -> bool:
    """ Инициализация микросервиса () """
    # настройка логирования
    logger.add(GC_LOG_FILE,
        rotation="500 MB",
        compression="zip",
        level="DEBUG",
        serialize=True)
    # настроечные параметры
    lo_config = Config()
    # запуск web-сервера
    uvicorn.run(io_app, host=lo_config.localhost_ip, port=lo_config.localhost_port)  # TODO async
    # возвращаем результат
    return True

@logger.catch
def run_one(is_url: str) -> list[str]:
    """
    Одиночный запуск (основная бизнес-логика)

    Args:
        is_url (str): URL обрабатываемого GitHub-репозитория

    Returns:
        list[str]: перечень путей к новым файлам (по умолчанию - [])
    """

    # значение по умолчанию
    ra_result = []
    # скачиваем репозиторий
    logger.info("[1/4]. Скачиваем Git-репозиторий")
    ls_folder = Tool.download_github_repo(is_url)
    # получаем список файлов
    logger.info("[2/4]. Получаем список файлов")
    la_file = Tool.get_all_files(ls_folder)
    # обрабатываем каждый файл
    li_count = len(la_file)
    logger.info(f"[3/4]. Запуск обработки {li_count} файлов")
    with trange(li_count) as t:
        for i in t:
            # анализируем (нужно ли обрабатывать)
            ls_file = la_file[i]
            t.set_description(f'Файл "{ls_file}"')
            ls_ext = Tool.get_file_extension(ls_file)
            lb_add = True
            ls_postfix = ""         
            match ls_ext:
                case ".py" | ".ipynb":
                    # добавляем комментарии в файл
                    ls_postfix = "обрабатывается"
                case _:
                    # пропускаем
                    ls_postfix = "пропущен"
                    lb_add = False
            t.set_postfix(loss=ls_postfix)
            # добавляем комментарии в файл
            if lb_add:
                AiAgent().run(C_TYPE_AGENT.ADD_COMMENT, ls_file)
            t.set_postfix(loss="готово")
    logger.info("[4/4]. Обработка завершена")
    # возвращаем результат
    return ra_result

if __name__ == "__main__":
    # Пример использования
    run_one("https://github.com/nyatsun/calc_and_win")
