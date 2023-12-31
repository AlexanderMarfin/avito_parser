# Словарь с локалями
LEXICON_RU: dict[str, str] = {
    "/start": "Добро пожаловать!\n\n"
    "Выберите, что будем делать или "
    "отправьте команду /help",
    "/help": "<b>Выгрузка объявлений</b> – выгрузка с сайта авито по ссылке.\n"
    "Ссылка должна быть в формате: https://www.avito.ru/регион/avtomobili/.../.../...\n\n"
    "<b>Поиск авто</b> – формирование ссылки на поиск и выгрузка по заданным параметрам авто.\n"
    "Будьте внимательны при указании города поиска!\n\n"
    "Максимальное количество выгрузки объявлений за один раз - 1000.",
    "/reset": "Правильно! Иногда стоит начать заново",
    "no_echo": "Данный тип апдейтов не поддерживается " "методом send_copy",
    "unloading": "📜Выгрузка объявлений",
    "unloading_choose": "Какие объявления хотим выгрузить?",
    "in_progress": "⚙️Данная функция в разработке",
    "unloading_auto": "Вставьте ссылку на поиск авто",
    "wrong_auto_link": f'Ссылка должна быть в формате: <a href="https://www.avito.ru/регион/avtomobili/">https://www.avito.ru/регион/avtomobili/.../.../...</a>',
    "auto_finder": "🚗Поиск авто",
    "auto_parse": "🚗Авто",
    "flat_parse": "🏢Квартиры",
    "link": "Ссылка",
    "next": "Дальше",
    "add": "Добавить",
    "exit": "Выйти",
    "skip": "Пропустить",
    "back": "🔙Назад",
    "retry": "Повторить",
    "start_parsing": "Поиск и выгрузка объявлений",
    "reset_data": "Начать заполнение заново",
    "info": "Статистика",
    "plot": "График",
    "menu": "Вернуться в меню",
    "description": "Описание",
    "automatic": "Автомат",
    "variable": "Вариатор",
    "robotic": "Робот",
    "manual": "Механика",
    "petrol": "Бензин",
    "diesel": "Дизель",
    "electric": "Электро",
    "gas": "Газ",
    "hybrid": "Гибрид",
    "rear-wheel": "Задний",
    "front-wheel": "Передний",
    "four-wheel": "Полный",
    "geo": "Геопозиция",
    "radius": "Радиус",
    "mark": "Марка",
    "model": "Модель",
    "transmission": "Трансмиссия",
    "engine": "Двигатель",
    "gear": "Привод",
    "price_from": "Цена от",
    "price_to": "Цена до",
    "year_from": "Год от",
    "year_to": "Год до",
    "mileage_from": "Пробег от",
    "mileage_to": "Пробег до",
    "try_again": "Попробуйте еще раз",
    "unknown": "Не понимаю, о чём вы",
    "check_data": "Проверьте данные для поиска:",
    "generate": "Генерируем ссылку поиска. Это займёт около 2 минут...",
    "time_to_unload": "Ваш запрос в очереди.\nПодсчет времени на выгрузку. Подождите несколько минут...",
    "ads_found": "Найдено объявлений: ",
    "unloading_time": "\nВыгрузка займёт около ",
    "minutes": " мин.",
    "not_found": "Ничего не нашлось :(",
    "many_ads": "Объявлений больше 1000. Пожалуйста, уточните поиск",
    "check_search": "\nМожет стоит расширить поиск?",
    "check_input": "\nПроверьте правильность ввода города, марки и модели",
    "parse_error": "Мы испытываем технические неполадки :(\nПопробуйте заново или воспользуйтесь прямой выгрузкой по ссылке",
    "timeout_error": "Сессия закрылась по таймауту. Попробуйте начать заново",
    "something_wrong": "Что-то пошло не так :(",
    "do_next": "Что будем делать дальше?",
    "input_city": "Введите город поиска, область, край или республику",
    "input_wrong_city": "Название должно быть написано кириллицей и не содержать других символов",
    "input_radius": "Введите радиус поиска (0, 50, 75, 100, 200, 300, 400, 500, 1000, 2000, 3000 км)",
    "input_wrong_radius": "Радиус поиска должен быть одним из таких 0, 50, 75, 100, 200, 300, 400, 500, 1000, 2000, 3000 км",
    "input_mark": "Введите марку авто",
    "input_wrong_name": "Возможно вы имели в виду ",
    "input_model": "Введите модель авто",
    "input_transmission": "Выберите тип трансмиссии",
    "input_wrong_transmission": "Выберите тип трансмиссии из предложенных вариантов",
    "input_engine": "Выберите тип двигателя",
    "input_wrong_engine": "Выберите тип двигателя из предложенных вариантов",
    "input_gear": "Выберите тип привода",
    "input_wrong_gear": "Выберите тип привода из предложенных вариантов",
    "input_price_from": "Введите начальную цену (Больше 0)",
    "input_wrong_price_from": "Цена должна быть не меньше 0 и состоять из цифр",
    "input_price_to": "Введите конечную цену\n(Больше ",
    "input_wrong_price_to": "Введите конечную цену\n(Должна быть больше начальной и состоять из цифр)",
    "input_year_from": "Введите начальный год (в диапазоне от 1960 до 2023)",
    "input_wrong_year_from": "Год должен быть в диапазоне от 1960 до 2023",
    "input_year_to": "Введите конечный год (от ",
    "input_wrong_year_to": "Конечный год должен быть больше начального и не больше 2023",
    "input_year_to_1": " до 2023)",
    "input_mileage_from": "Введите начальный пробег (от 0 и кратный 10000)",
    "input_wrong_mileage_from": "Пробег должен быть больше начального, состоять из цифр и быть кратным 10000",
    "input_mileage_to": "Введите конечный пробег (от ",
    "input_wrong_mileage_to": "Пробег должен быть больше начального, состоять из цифр и быть кратным 10000",
    "input_mileage_to_1": " и кратный 10000)",
    "input_mileage_to_2": "Введите конечный пробег (больше начального и кратный 10000)",
}
