import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from config_data.config import Config, load_config
from handlers import other_handlers, menu_handlers, auto_handlers, commands_handlers, errors_handlers
from middlewares.throttling_middleware import ThrottlingMiddleware
from middlewares.webdriver_middleware import WebdriverMiddleware
import database.models


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Подключаемся к БД
    database.models.register_models()

    # Подключаемся к Redis
    storage = RedisStorage.from_url("redis://localhost:6379/0")

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    # Регистрируем мидлвари
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
    dp.callback_query.middleware.register(WebdriverMiddleware(storage=storage))
    dp.message.middleware.register(WebdriverMiddleware(storage=storage))
    dp.message.middleware.register(ChatActionMiddleware())

    # Регистриуем роутеры в диспетчере
    dp.include_router(errors_handlers.router)
    dp.include_router(commands_handlers.router)
    dp.include_router(menu_handlers.router)
    dp.include_router(auto_handlers.router)
    dp.include_router(other_handlers.router)

    # Запускаем polling и принимаем накопившиеся апдейты
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
