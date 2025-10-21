"""
Обработчики медиафайлов
"""
from aiogram import Router, F
from aiogram.types import Message

# Создаем роутер для медиафайлов
media_router = Router()


@media_router.message(F.photo)
async def handle_photo(message: Message):
    """Обработчик фотографий"""
    photo_text = (
        "📸 Получено фото!\n\n"
        "В данный момент бот не обрабатывает изображения.\n"
        "Используйте текстовые сообщения для добавления привычек."
    )
    await message.answer(photo_text)


@media_router.message(F.video)
async def handle_video(message: Message):
    """Обработчик видео"""
    video_text = (
        "🎥 Получено видео!\n\n"
        "В данный момент бот не обрабатывает видео.\n"
        "Используйте текстовые сообщения для добавления привычек."
    )
    await message.answer(video_text)


@media_router.message(F.document)
async def handle_document(message: Message):
    """Обработчик документов"""
    doc_text = (
        "📄 Получен документ!\n\n"
        "В данный момент бот не обрабатывает документы.\n"
        "Используйте текстовые сообщения для добавления привычек."
    )
    await message.answer(doc_text)


@media_router.message(F.voice)
async def handle_voice(message: Message):
    """Обработчик голосовых сообщений"""
    voice_text = (
        "🎤 Получено голосовое сообщение!\n\n"
        "В данный момент бот не обрабатывает голосовые сообщения.\n"
        "Используйте текстовые сообщения для добавления привычек."
    )
    await message.answer(voice_text)
