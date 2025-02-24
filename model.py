import os

from huggingface_hub import InferenceClient


def prompts(type_, question, news, answers, reasoning):
    req = {
        "url": f"""Ниже представлен список ссылок на разделы новостного сайта ИТМО и подробная расшифровка для них. Выбери до трех разделов, которые наиболее вероятно содержат ответ на вопрос пользователя: <question>{question}</question>
        
1. Наука (<url>https://news.itmo.ru/ru/science/</url>)

Описание: Раздел «Наука» посвящен освещению научно-исследовательской деятельности Университета ИТМО. Здесь публикуются новости о последних открытиях, исследованиях, грантах, научных проектах и достижениях ученых университета.
Назначение: Информировать широкую аудиторию о передовых научных разработках, продвигаемых университетом, и демонстрировать вклад ИТМО в развитие мировой науки.
2. IT (<url>https://news.itmo.ru/ru/science/it/</url>)

Описание: Раздел «IT» специализируется на новостях и событиях в сфере информационных технологий. Здесь представлены материалы о разработках в области программирования, искусственного интеллекта, кибербезопасности и других IT-направлений, которые ведутся в университете.
Назначение: Отображать актуальные тенденции и достижения ИТМО в области информационных технологий, привлекать интерес специалистов и студентов к новым исследованиям и проектам.
3. Фотоника (<url>https://news.itmo.ru/ru/science/photonics/</url>)

Описание: Раздел «Фотоника» посвящен новостям и исследованиям в области фотоники — науки о световых технологиях. Здесь размещаются материалы о разработке новых оптических систем, лазеров, волоконно-оптических технологий и их применении.
Назначение: Представлять достижения университета в области фотоники, способствовать развитию этой науки и привлекать интерес к исследовательским инициативам в данной сфере.
4. Киберфизика (<url>https://news.itmo.ru/ru/science/cyberphysics/</url>)

Описание: «Киберфизика» фокусируется на интеграции физических систем и информационных технологий. Раздел освещает разработки в области робототехники, автоматизации, встроенных систем и Интернета вещей (IoT), проводимые в ИТМО.
Назначение: Демонстрировать междисциплинарные проекты, объединяющие физику и информатику, и подчеркивать инновационный подход университета к созданию киберфизических систем.
5. Новые материалы (<url>https://news.itmo.ru/ru/science/new_materials/</url>)

Описание: Раздел посвящен исследованиям в области создания и изучения новых материалов с уникальными свойствами, включая наноматериалы, композиты и биоматериалы.
Назначение: Освещать передовые научные работы по материаловедению, демонстрируя вклад ИТМО в развитие технологий нового поколения.
6. LifeScience (<url>https://news.itmo.ru/ru/science/life_science/</url>)

Описание: Раздел «LifeScience» охватывает биологические и биомедицинские исследования университета. Здесь публикуются новости о биотехнологиях, генетических исследованиях, биоинформатике и смежных областях.
Назначение: Продвигать научные достижения в областях, связанных с жизненными науками, и информировать об их практическом применении.
7. Образование (<url>https://news.itmo.ru/ru/education/</url>)

Описание: Раздел «Образование» посвящен образовательным программам и мероприятиям ИТМО. Здесь размещаются новости о новых курсах, образовательных инициативах, реформах и педагогических практиках.
Назначение: Информировать студентов, абитуриентов и педагогов о возможностях обучения и развития в университете.
8. Сотрудничество (<url>https://news.itmo.ru/ru/education/cooperation/</url>)

Описание: Этот раздел освещает партнерские проекты университета с другими образовательными учреждениями, международные программы обмена и совместные учебные инициативы.
Назначение: Представлять возможности для академического сотрудничества и международного взаимодействия, способствовать обмену опытом и знаниями.
9. Тренды (<url>https://news.itmo.ru/ru/education/trend/</url>)

Описание: Раздел «Тренды» фокусируется на современных тенденциях в образовании и науке. Здесь обсуждаются инновационные методики обучения, технологии EdTech и глобальные изменения в образовательной среде.
Назначение: Информировать о новейших трендах, влияющих на будущее образования, и позиционировать ИТМО как передовой образовательный центр.
10. Студенты (<url>https://news.itmo.ru/ru/education/students/</url>)

Описание: Этот раздел посвящен студенческой жизни: успехам, инициативам, проектам и мероприятиям, организованным студентами.
Назначение: Поддерживать студенческое сообщество, делиться историями успеха и вдохновлять на активное участие в жизни университета.
11. Официально (<url>https://news.itmo.ru/ru/education/official/</url>)

Описание: «Официально» содержит официальные заявления, приказы и информацию от руководства университета, касающуюся образовательного процесса и административных вопросов.
Назначение: Обеспечивать прозрачность и доступность важной официальной информации для всех членов университетского сообщества.
12. Стартапы и бизнес (<url>https://news.itmo.ru/ru/startups_and_business/</url>)

Описание: Раздел посвящен предпринимательской деятельности, инновационным проектам и стартапам, возникающим на базе университета или при его поддержке.
Назначение: Поддерживать культуру предпринимательства, предоставляя информацию о возможностях развития бизнеса и успешных кейсах.
13. Бизнес-успех (<url>https://news.itmo.ru/ru/startups_and_business/business_success/</url>)

Описание: Здесь публикуются истории успеха компаний, основанных выпускниками или сотрудниками ИТМО, а также значимых достижений в бизнес-сфере.
Назначение: Вдохновлять на предпринимательство, демонстрируя реальные примеры успешного развития бизнес-проектов.
14. Инновации (<url>https://news.itmo.ru/ru/startups_and_business/innovations/</url>)

Описание: Раздел «Инновации» освещает передовые технологические разработки и инновационные решения, созданные в университете.
Назначение: Показывать лидерство ИТМО в инновационной деятельности и стимулировать интерес к новым технологиям.
15. Будни стартапа (<url>https://news.itmo.ru/ru/startups_and_business/startup/</url>)

Описание: Этот раздел рассказывает о повседневной жизни стартапов, их развитии, преодолении трудностей и достижениях.
Назначение: Предоставлять инсайты и практический опыт начинающим предпринимателям, показывая реальное положение дел в стартап-среде.
16. Партнерство (<url>https://news.itmo.ru/ru/startups_and_business/partnership/</url>)

Описание: Раздел посвящен сотрудничеству университета с бизнесом, промышленными предприятиями и международными организациями.
Назначение: Освещать совместные проекты и программы, демонстрируя преимущества партнерства с ИТМО.
17. Инициативы (<url>https://news.itmo.ru/ru/startups_and_business/initiative/</url>)

Описание: Здесь представлены новые инициативы, программы поддержки и мероприятия, направленные на развитие предпринимательской активности.
Назначение: Поощрять инновационное мышление и участие в проектах, способствующих экономическому росту и развитию технологий.
18. Жизнь университета (<url>https://news.itmo.ru/ru/university_live/</url>)

Описание: «Жизнь университета» объединяет новости о внутренних событиях, праздниках, культурных и спортивных мероприятиях, происходящих в ИТМО.
Назначение: Создавать ощущение единства университетского сообщества, информируя о разнообразных аспектах жизни в ИТМО.
19. Рейтинги (<url>https://news.itmo.ru/ru/university_live/ratings/</url>)

Описание: Раздел освещает позиции ИТМО в национальных и международных рейтингах, а также достижения в области академической репутации.
Назначение: Подчеркивать высокие стандарты университета и его признание на мировой арене.
20. Достижения (<url>https://news.itmo.ru/ru/university_live/achievements/</url>)

Описание: Здесь публикуются новости о значимых успехах студентов, преподавателей и коллективов университета в различных областях.
Назначение: Признавать и поощрять достижения членов университета, мотивировать на новые высоты.
21. Досуг (<url>https://news.itmo.ru/ru/university_live/leisure/</url>)

Описание: Раздел «Досуг» рассказывает о возможностях для отдыха и развлечений: клубах по интересам, спортивных секциях, культурных мероприятиях.
Назначение: Обеспечивать информацию о способах проведения свободного времени, способствуя балансу между учебой и отдыхом.
22. Объявления (<url>https://news.itmo.ru/ru/university_live/ads/</url>)
Описание: Этот раздел содержит важные объявления и уведомления для студентов и сотрудников университета.
Назначение: Быстро и эффективно информировать о предстоящих событиях, изменениях в расписании, собраниях и других актуальных новостях.
23. Социальная активность (<url>https://news.itmo.ru/ru/university_live/social_activity/</url>)
Описание: Раздел посвящен социальным проектам и волонтерским инициативам, в которых участвуют студенты и сотрудники ИТМО.
Назначение: Поощрять участие в общественно полезных делах, развивать социальную ответственность и активность.
24. Медиа (<url>https://news.itmo.ru/ru/media/</url>)
Описание: «Медиа» включает в себя фотогалереи, видеоматериалы, подкасты и другие мультимедийные ресурсы, связанные с жизнью университета.
Назначение: Предоставлять визуальный и аудиоконтент, дополняющий текстовые материалы и создающий полное представление о событиях в ИТМО.
25. Блог (<url>https://news.itmo.ru/ru/blogs/</url>)
Описание: Раздел «Блог» является площадкой для личных заметок, мнений и статей от членов университетского сообщества: студентов, преподавателей и сотрудников.
Назначение: Служить средством свободного обмена идеями, опытом и знаниями, способствовать развитию внутренней коммуникации и самовыражения.

Верни ответ в формате json-словаря названий раздела и ссылок
Best practice answer: {{"<name1>": "<url1>", "<name2>": "<url2>"}}""",

    "reson": f"""Вот пример промпта для модели, которая должна провести рассуждение по предоставленным новостям и ответить на вопрос пользователя:

Инструкция для модели:
Вы выступаете в роли аналитика новостей Университета ИТМО. Ваша задача — прочитать предоставленные новости из различных разделов портала и ответить на вопрос пользователя, основываясь на этой информации.

Шаги для выполнения задачи:
Внимательно прочитайте вопрос пользователя.
Изучите предоставленные новости, обращая внимание на разделы, которые могут быть связаны с вопросом.
Выделите ключевую информацию из новостей, которая относится к вопросу.
Сформулируйте ответ на вопрос пользователя, используя найденную информацию.
Объясните свой ответ, ссылаясь на конкретные факты из новостей.

Правила:
Предоставляйте точную и проверенную информацию.
Избегайте домыслов и предположений без оснований.
Сохраняйте нейтральный и уважительный тон.
Если в новостях нет информации, необходимой для ответа, вежливо сообщите об этом пользователю.

Вопрос пользователя:
{question}

Новости:
{news}

Пример ответа:
"D разделе «[Название раздела]» сообщается, что... [далее следует подробный ответ на вопрос пользователя с указанием источников информации из новостей]."

Примечание:
Убедитесь, что все ссылки на разделы новостей и их описания соответствуют содержанию.
Пишите ответ полностью своими словами, не копируя текст напрямую из новостей.
Стремитесь к ясности и точности в изложении информации.""",

    "answer": f"""Тебе необходимо ответить на вопрос пользователя, выбрав правильный вариант ответа из пронумерованных вариантов ответа.        В качетсве ответа предоставь только номер правильного ответа
Другой ассистент дал следующий развернутый ответ на этот вопрос: {reasoning}

Ориентируйся на показания ассистента и свои знания. Дай ответ только в виде числа, обозначающего номер верного ответа

Вопрос пользователя: {question}
Варианты ответа на вопрос: {answers}"""}
    
    return req[type_]
    

def model_request_urls(question, answers, sources):
    client = InferenceClient(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        api_key=os.environ['API_HF']
    )

    messages = [
        {
            "role": "user",
            "content": prompts('url', question, None, None, None)
        }
    ]

    stream = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
        messages=messages, 
        max_tokens=300,
        temperature=0
    )
    return stream.choices[0].message.content

def model_request_reasoning(question, news):
    client = InferenceClient(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        api_key=os.environ['API_HF']
    )

    messages = [
        {
            "role": "user",
            "content": prompts('reson', question, news, None, None)
        }
    ]

    stream = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
        messages=messages, 
        max_tokens=200,
        temperature=0
    )
    return stream.choices[0].message.content

def model_request_answer(question, answers, reasoning):
    client = InferenceClient(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        api_key=os.environ['API_HF']
    )

    messages = [
        {
            "role": "user",
            "content": prompts('answer', question, None, answers, reasoning)
        }
    ]

    stream = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
        messages=messages, 
        max_tokens=2,
        temperature=0
    )
    return stream.choices[0].message.content