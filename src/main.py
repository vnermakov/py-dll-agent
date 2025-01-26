from loguru import logger                                           # pip install loguru
from fastapi import FastAPI, Request                                # pip install fastapi
from fastapi.responses import PlainTextResponse, JSONResponse
from config import Config
from main_api import run_init, run_one

# глобальные переменные
app = FastAPI()

# ROUTES:

@app.middleware("http")
@logger.catch
async def api_log_requests(request: Request, call_next):
    """ Логирование REST-запросов """
    logger.debug(f"Запрос: {request.method} {request.url}")
    response = await call_next(request)
    logger.debug(f"Ответ: {response.status_code}")
    return response

@app.get("/")
@logger.catch
async def api_root():
    """ Проверка доступности REST-сервиса """
    lo_config = Config()
    return f"REST-сервис доступен (Swagger - http://{lo_config.localhost_ip}:{lo_config.localhost_port}/redoc)"

@app.get("/run_one")
@logger.catch
async def api_run_one():
    """ Одиночный запуск основной логики """
    run_one("https://github.com/nyatsun/calc_and_win")
    return "Запрос обработан"

# локальный запуск
if __name__ == '__main__':
    run_init(app)