"""
Основной файл бота-трекера привычек
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Импорты конфигурации
from config import BOT_TOKEN

# Импорты роутеров
from handlers import commands, text, media, callbacks

# Импорты утилит
from utils.reminder_service import init_reminder_service

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция запуска бота"""
    # Создаем экземпляры бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Инициализируем сервис напоминаний
    reminder_service = init_reminder_service(bot)
    logger.info("Сервис напоминаний инициализирован")
    
    # Регистрируем роутеры
    dp.include_router(commands.commands_router)
    dp.include_router(text.text_router)
    dp.include_router(media.media_router)
    dp.include_router(callbacks.callback_router)
    
    logger.info("Бот запущен!")
    
    try:
        # Запускаем бота
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
