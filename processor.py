import re
from model import model_request_urls, model_request_reasoning, model_request_answer
from scraper import scrapping_websites


def process_answer(query):
    pattern = r"^(.*?)\s*\n(1\..*)"
    match = re.match(pattern, query, re.DOTALL)
    question = None
    answers = None

    if match:
        # Извлечение вопроса и вариантов ответа
        question = match.group(1).strip()
        answers = match.group(2).strip().split("\n")
    else:
        pattern = r"^(.*?)\?"
        match = re.match(pattern, query, re.DOTALL)
        question = match.group(1).strip()


    # Запрос к модели для поиска релевантных ссылок
    urls = model_request_urls(question, answers, None)
    
    pattern = r"https?://[^\s\"']+"
    # Извлекаем все совпадения (ссылки) из ответа
    urls = re.findall(pattern, urls)
    

    # Парсинг контента по ссылкам
    parsed_urls = scrapping_websites(urls)
    reasoning = model_request_reasoning(question, parsed_urls)

    # выдача ответа на вопрос
    if answers is not None:
        answer = model_request_answer(question, answers, reasoning)
        pattern = r"\d+"
        answer = re.findall(pattern, answer)
        if not answer:
            answer = 1
        return int(answer[0]), reasoning, urls
    else:
        return "null", reasoning, urls