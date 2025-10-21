"""
Обработчики команд бота
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import requests
from config import QUOTES_URL
import random
from bs4 import BeautifulSoup

# Создаем роутер для команд
commands_router = Router()


@commands_router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Я - бот для отслеживания привычек.\n\n"
        "С моей помощью ты сможешь:\n"
        "• Добавлять новые привычки\n"
        "• Отмечать выполнение привычек\n"
        "• Просматривать статистику\n\n"
        "Используй /help для получения списка команд."
    )
    await message.answer(welcome_text)


@commands_router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📋 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/menu - Открыть главное меню\n"
        "/date - Парсинг дат\n"
        "/reminders - Управление напоминаниями\n"
        "/quotes - мотивационные цитаты\n\n"
        "💡 Совет: Используй кнопки меню для удобной навигации!"
    )
    await message.answer(help_text)


@commands_router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Обработчик команды /menu - открывает главное меню"""
    from keyboards.main_menu import get_main_menu_keyboard
    
    menu_text = (
        "🏠 Главное меню\n\n"
        "Выберите действие:"
    )
    await message.answer(
        menu_text,
        reply_markup=get_main_menu_keyboard()
    )


@commands_router.message(Command("date"))
async def cmd_date(message: Message):
    """Обработчик команды /date - парсинг дат"""
    from utils.date_parser import date_parser
    
    help_text = (
        "📅 Парсинг дат\n\n"
        "Отправьте мне дату в любом из форматов:\n\n"
        "• Сегодня, завтра, вчера\n"
        "• 25.12.2024, 2024-12-25\n"
        "• Понедельник, вторник, среда...\n"
        "• Через 3 дня, через 2 недели\n"
        "• 15.12 (текущий год)\n\n"
        "Пример: 'напомни мне завтра в 9:00'"
    )
    await message.answer(help_text)


@commands_router.message(Command("reminders"))
async def cmd_reminders(message: Message):
    """Обработчик команды /reminders - управление напоминаниями"""
    from utils.reminder_service import get_reminder_service
    
    reminder_service = get_reminder_service()
    if not reminder_service:
        await message.answer("❌ Сервис напоминаний не инициализирован")
        return
    
    stats = reminder_service.get_reminder_stats(message.from_user.id)
    
    reminders_text = (
        f"🔔 Ваши напоминания\n\n"
        f"Активных напоминаний: {stats['active_reminders']}\n"
        f"Всего напоминаний: {stats['total_reminders']}\n\n"
        "Используйте /help для получения списка команд."
    )
    await message.answer(reminders_text)


@commands_router.message(Command("quotes"))
async def cmd_quote(message: Message):
    """Обработчик команды /quotes - отправляет цитаты"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Делаем запрос к сайту
        response = requests.get(QUOTES_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Проверяем успешность запроса

        # Парсим HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим все цитаты (они находятся в div с классом field-item even)
        quotes = soup.find_all('div', class_='field-name-body')

        if not quotes:
            await message.answer("Цитаты не найдены")
            return None

        # Фильтруем только те элементы, которые содержат текст цитат
        quote_texts = []
        for quote in quotes:
            # Ищем параграфы внутри цитат
            paragraphs = quote.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and len(text) > 10:  # Отсеиваем короткие тексты
                    quote_texts.append(text)

        if not quote_texts:
            await message.answer("В цитатах нет ничего")
            return None

        random_quote = random.choice(quote_texts)
        await message.answer(f"Цитата для тебя:\n{random_quote}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
