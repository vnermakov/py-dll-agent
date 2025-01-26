import os
from dotenv import load_dotenv, set_key, find_dotenv                # pip install load_dotenv
from loguru import logger                             
from typing import Optional
from const import GC_LOG_FILE, GC_ENV_FILE, GC_LOCALHOST_IP, GC_LOCALHOST_PORT

class Config:
    env: str                                                        # тип окружения (DEV|QAS|PRD)
    # локальный хост
    localhost_ip: str = GC_LOCALHOST_IP                             # IP-адрес
    localhost_port: int = GC_LOCALHOST_PORT                         # порт
    localhost_log_file: str = GC_LOG_FILE                           # файл логирования
    # служебные
    mb_init: bool = False                                           # флаг успешной инициализации
    
    @logger.catch
    def __init(self, iv_env: Optional[str] = None):
        # принудительно загружаем переменные из .env файла (нужно для Docker)
        load_dotenv()
        # тип окружения (DEV|QAS|PRD)
        if iv_env is not None:
            lv_env = iv_env
        else:
            lv_env = os.environ.get("ENV")
        self.env = lv_env
        # основные параметры
        self.refresh()
        # служебные (поднимаем флаг окончания инициализации)
        self.__mb_init = True

    @logger.catch
    def check(self) -> bool:
        return self.__mb_init

    @logger.catch
    def refresh(self) -> bool:
        # принудительно загружаем переменные из .env файла (нужно для Docker)
        load_dotenv()
        # основные параметры:
        self.localhost_ip = os.environ.get("LOCALHOST_IP")
        self.localhost_port = int(os.environ.get("LOCALHOST_PORT"))
        self.localhost_log_file = GC_LOG_FILE
        # возвращаем результат
        return True
