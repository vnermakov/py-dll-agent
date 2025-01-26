# системные библиотеки
#import os
from loguru import logger
from dotenv import load_dotenv
#import openai
#import langchain_core
#from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# библиотеки проекта
from const import C_TYPE_AGENT, GC_CODEPAGE, GC_URL_AI
from tool import Tool

# загрузка переменных окружения из файла .env
load_dotenv()

class AiAgent:
    """
    класс "AI-агент"
    """

    # глобальные переменные
    __mo_llm = None

    @logger.catch
    def __init__(self) -> bool:
        # инициализация языковой модели с явным указанием кодировки
        #self.__mo_llm = ChatOpenAI(temperature=0.7)                # OpenAI GPT-3.5
        self.__mo_llm = ChatOpenAI(
            api_key="not-needed",
            base_url=GC_URL_AI,                                     # LM Studio
            temperature=0.5
        )
    
    @logger.catch
    def __make_chain(self, ii_type: C_TYPE_AGENT, is_file_path: str) -> None:
        # значение по умолчанию
        ro_result = None
        # формируем system prompt
        ls_system = None
        match ii_type:
            case C_TYPE_AGENT.ADD_COMMENT:
                # обогащение кода комментариями
                ls_system = ( "Вы - опытный Python разработчик. Вы получаете от пользователя содержимое файла с Python-кодом. "
                    "Ваша задача - обогатить его комментариями и вернуть обратно пользователю только готовый исходный код для вставки обратно в файл (без своих пояснений)" )
                    #"Ваша задача - вернуть только обогащенный комментариями код, без дополнительных пояснений и без обрамления в символы ```." )
                    #"Ваша задача - обогатить его комментариями и вернуть готовый исходный код для вставки обратно в файл." )
            case C_TYPE_AGENT.GEN_DOC:
                # генерация документации
                ls_system = ( "Вы - опытный Python разработчик. Вы получаете от пользователя содержимое файла с Python-кодом. "
                    "Ваша задача - сгенерировать техническую документацию к коду и вернуть обратно пользователю только готовый текст для вставки обратно в файл" )
            case C_TYPE_AGENT.GEN_UT:
                # генерация unit-тестов
                ls_system = ( "Вы - опытный Python разработчик. Вы получаете от пользователя содержимое файла с Python-кодом. "
                    "Ваша задача - сгенерировать модульные тесты (библиотека pytest) для кода и вернуть обратно пользователю только готовый код" )
            case _:
                logger.error(f"В качестве параметра передан неизвестный тип агента - {ii_type}")
        # создание цепочки с использованием RunnableSequence
        if ls_system is not None:
            lo_prompt = ChatPromptTemplate.from_messages([
                ("system", ls_system),
                ("user", "{code}" )
            ])
            ro_result = lo_prompt | self.__mo_llm | StrOutputParser()
        # возвращаем результат
        return ro_result

    @logger.catch
    def run(self, ii_type: C_TYPE_AGENT, is_file_path: str) -> str|None:
        """
        Выполнить цепочку обработки файла

        Args:
            ii_type (C_TYPE_AGENT): тип агента
            is_file_path (str): путь к файлу

        Returns:
            str|None: путь к итоговому файлу (по умолчанию - None)
        """
        # значение по умолчанию
        rs_result = None
        # создание цепочки
        lo_chain = self.__make_chain(ii_type, is_file_path)
        if lo_chain is not None:
            # чтение содержимого файла с явным указанием кодировки
            with open(is_file_path, 'r', encoding=GC_CODEPAGE) as file:
                code = file.read()
            # получение комментированного кода от AI
            ls_postfix = ""
            match ii_type:
                case C_TYPE_AGENT.ADD_COMMENT:
                    # обогащение кода комментариями
                    ls_answer = lo_chain.invoke({"code": code})
                    ls_postfix = "_comment"
                case C_TYPE_AGENT.GEN_DOC:
                    # генерация документации
                    ls_answer = lo_chain.invoke({"code": code})
                    ls_postfix = "_doc"
                case C_TYPE_AGENT.GEN_UT:
                    # генерация unit-тестов
                    ls_answer = lo_chain.invoke({"code": code})
                    ls_postfix = "_ut"
                case _:
                    logger.error(f"В качестве параметра передан неизвестный тип агента - {ii_type}")
            ls_result = Tool.extract_code(ls_answer)
            # запись обновленного кода в новый файл с явным указанием кодировки
            ls_new = is_file_path.replace('.py', f'{ls_postfix}.py')
            with open(ls_new, 'w', encoding=GC_CODEPAGE) as file:
                file.write(ls_result)
                rs_result = ls_new
        # возвращаем результат
        return rs_result


# Использование функции
if __name__ == "__main__":
    ls_path = "/Users/evn/Desktop/AUXO/DLL-35/py-dll-agent/test/file/js_1.js"
    ls_path = "/Users/evn/Desktop/AUXO/DLL-35/py-dll-agent/test/file/python_1.py"
    lo_agent = AiAgent()
    lo_agent.run(C_TYPE_AGENT.ADD_COMMENT, ls_path)
    lo_agent.run(C_TYPE_AGENT.GEN_DOC, ls_path)
    lo_agent.run(C_TYPE_AGENT.GEN_UT, ls_path)