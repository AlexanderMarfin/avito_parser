# 🔍️ Avito_Parser
***
Бот предназначен для парсинга объявлений авито.
Текущая версия не финальная, бот находится в разработке.


## ⚙️ Установка
***
1. Создайте копию репозитория на своей машине `git clone https://github.com/AlexanderMarfin/avito_bot.git`
2. Переименуйте `.env.example` to `.env`
3. Заполните файл `.env` своими данными
4. Запустите бота
### 🐳 С помощью docker

Сборка
```shell
docker-compose -f docker-compose.yml up 
```
Установка chrome в контейнере бота
```shell
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update
apt install ./google-chrome-stable_current_amd64.deb
```

### 🛇 Без docker
```shell
pip install -r requirements.txt
python bot.py
```
## 🔩 Структура проекта
***
```
Avito_avtobot/
├── bot.py
├── config_data
│   ├── __init__.py
│   └── config.py
├── database
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── methods
│   │   ├── __init__.py
│   └── └── create.py
├── filters
│   ├── __init__.py
│   └── filters.py
├── handlers
│   ├── __init__.py
│   ├── auto_handlers.py
│   ├── commands_handlers.py
│   ├── errors_handlers.py
│   ├── handlers_utils.py
│   ├── menu_handlers.py
│   └── other_handlers.py
├── keyboards
│   ├── __init__.py
│   ├── kb_utils.py
│   └── keyboards.py
├── lexicon
│   ├── __init__.py
│   └── lexicon.py
├── middlewares
│   ├── __init__.py
│   ├── throttling_middleware.py
│   └── webdriver_middleware.py
├── misc
│   ├── __init__.py
│   └── singleton.py
├── parsers
│   ├── __init__.py
│   ├── auto_parsers.py
│   ├── objects.py
│   └── parser_utils.py
├── states
│   ├── __init__.py
│   └── user_states.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── bot.py


```
## 📂 Описание пакетов
***
- `config_data` Конфигурационные данныме
- `database` Взаимодействие с БД
- `filters` Кастомные фильтры
- `handlers` Обработчики апдейтов
- `keyboards` Билдеры клавиатур
- `lexicon` Языковой пакет
- `middlewares` Мидлвари
- `parsers` Парсеры Авито
- `states` Машина состояний
- `misc` Прочее

## ⚒️ Использование
***
- /start - запуск бота
- /restart - перезапуск в любой непонятной ситуации
- /help - помощь

### 🔘 Меню выбора
***
![Home_menu](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/c310efae-f6ff-4d00-b163-3149ae79392a)

Бот позволяет сделать прямую выгрузку по ссылке авито или выполнить интеркативный поиск по параметрам авто

### 🔗 Выгрузка объявлений по ссылке
***
![Unloading_menu](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/4318709e-9992-4855-bd82-7c59cb182e08)

Выполните поиск на сайте авито и отправьте ссылку боту

![Auto_parsing](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/69fc031e-e296-4b88-83cb-77d36208197c)

Файл с выгрузкой будет доступен в формате csv

![File](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/ca673b90-23f1-4fcf-abe5-7174733610e0)

Бот предлагает базовый анализ выгруженных данных. Учитываются только те объявления, где нет пропущенных значений 

Статистика

![stats](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/dede5cad-1375-4a1b-9ad7-77aece8af142)

График

![plot](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/da67da05-3619-463e-9365-4d5ee448fecd)

### 🌟 Генератор ссылки с последующей выгрузкой
***
Интерактивный режим поиска авто по передаваемым параметрам

![Auto_Finder](https://github.com/AlexanderMarfin/avito_parser/assets/128323460/911786a7-87b7-4423-aae8-9c0a3175f055)
