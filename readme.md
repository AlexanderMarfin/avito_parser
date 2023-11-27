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
![Home_menu.png](..%2F..%2FDesktop%2FHome_menu.png)

Бот позволяет сделать прямую выгрузку по ссылке авито или выполнить интеркативный поиск по параметрам авто

### 🔗 Выгрузка объявлений по ссылке
***
![Unloading_menu.png](..%2F..%2FDesktop%2FUnloading_menu.png)

Выполните поиск на сайте авито и отправьте ссылку боту

![Auto_parsing.png](..%2F..%2FDesktop%2FAuto_parsing.png)

Файл с выгрузкой будет доступен в формате csv

![File.png](..%2F..%2FDesktop%2FFile.png)

Бот предлагает базовый анализ выгруженных данных. Учитываются только те объявления, где нет пропущенных значений 

Статистика

![stats.jpg](..%2F..%2FDesktop%2Fstats.jpg)

График

![plot.jpg](..%2F..%2FDesktop%2Fplot.jpg)

### 🌟 Генератор ссылки с последующей выгрузкой
***
Интерактивный режим поиска авто по передаваемым параметрам

![Auto_Finder.png](..%2F..%2FDesktop%2FAuto_Finder.png)
