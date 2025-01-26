import enum

@enum.unique
class C_TYPE_AGENT(enum.Enum):
    ADD_COMMENT = 1                                                 # добавить комментарии в файл
    GEN_DOC = 2                                                     # сгенерировать документацию        
    GEN_UT = 3                                                      # сгенерировать unit-тесты

# прочие константы
GC_ENV_FILE: str = ".env"                                           # ENV-файл 
GC_LOG_FILE: str = "logs/app.log"                                   # файл логирования
GC_LOCALHOST_IP: str = "127.0.0.1"                                  # IP-адрес REST-сервиса
GC_LOCALHOST_PORT: int = 8000                                       # номер порта REST-сервиса
GC_URL_AI: str = "http://localhost:1234/v1"                         # URL AI-сервиса (LM Studio)
GC_CODEPAGE: str = "utf-8"                                          # кодировка файлов