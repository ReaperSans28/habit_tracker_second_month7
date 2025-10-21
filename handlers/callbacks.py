"""
Обработчики callback запросов от inline кнопок
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_habit_actions_keyboard, get_confirmation_keyboard

# Создаем роутер для callback запросов
callback_router = Router()


@callback_router.callback_query(F.data.startswith("habit_done_"))
async def handle_habit_done(callback: CallbackQuery):
    """Обработчик отметки привычки как выполненной"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("✅ Привычка отмечена как выполненная!")
    await callback.message.edit_text(
        f"✅ Привычка #{habit_id} отмечена как выполненная!\n\n"
        "Отличная работа! Продолжайте в том же духе! 🎉"
    )


@callback_router.callback_query(F.data.startswith("habit_skip_"))
async def handle_habit_skip(callback: CallbackQuery):
    """Обработчик пропуска привычки"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("❌ Привычка пропущена")
    await callback.message.edit_text(
        f"❌ Привычка #{habit_id} пропущена.\n\n"
        "Не расстраивайтесь! Завтра новый день! 💪"
    )


@callback_router.callback_query(F.data.startswith("habit_edit_"))
async def handle_habit_edit(callback: CallbackQuery):
    """Обработчик редактирования привычки"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("✏️ Редактирование привычки")
    await callback.message.edit_text(
        f"✏️ Редактирование привычки #{habit_id}\n\n"
        "Функция редактирования будет добавлена в следующих уроках."
    )


@callback_router.callback_query(F.data.startswith("habit_delete_"))
async def handle_habit_delete(callback: CallbackQuery):
    """Обработчик удаления привычки"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("🗑️ Удаление привычки")
    await callback.message.edit_text(
        f"🗑️ Удаление привычки #{habit_id}\n\n"
        "Вы уверены, что хотите удалить эту привычку?",
        reply_markup=get_confirmation_keyboard("delete", habit_id)
    )


@callback_router.callback_query(F.data.startswith("habit_stats_"))
async def handle_habit_stats(callback: CallbackQuery):
    """Обработчик просмотра статистики привычки"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("📊 Статистика привычки")
    await callback.message.edit_text(
        f"📊 Статистика привычки #{habit_id}\n\n"
        "Функция статистики будет добавлена в следующих уроках."
    )


@callback_router.callback_query(F.data.startswith("select_habit_"))
async def handle_select_habit(callback: CallbackQuery):
    """Обработчик выбора привычки"""
    habit_index = callback.data.split("_")[-1]
    
    await callback.answer(f"Выбрана привычка #{habit_index}")
    await callback.message.edit_text(
        f"📝 Привычка #{habit_index}\n\n"
        "Выберите действие:",
        reply_markup=get_habit_actions_keyboard(habit_index)
    )


@callback_router.callback_query(F.data == "add_new_habit")
async def handle_add_new_habit(callback: CallbackQuery):
    """Обработчик добавления новой привычки"""
    await callback.answer("➕ Добавление новой привычки")
    await callback.message.edit_text(
        "➕ Добавление новой привычки\n\n"
        "Напишите название привычки, которую хотите отслеживать.\n\n"
        "Например: 'Читать 30 минут в день' или 'Делать зарядку'"
    )


@callback_router.callback_query(F.data.startswith("confirm_"))
async def handle_confirmation(callback: CallbackQuery):
    """Обработчик подтверждения действия"""
    action = callback.data.split("_")[1]
    item_id = callback.data.split("_")[2]
    
    if action == "delete":
        await callback.answer("✅ Привычка удалена!")
        await callback.message.edit_text(
            f"✅ Привычка #{item_id} удалена.\n\n"
            "Привычка успешно удалена из вашего списка."
        )


@callback_router.callback_query(F.data.startswith("cancel_"))
async def handle_cancellation(callback: CallbackQuery):
    """Обработчик отмены действия"""
    action = callback.data.split("_")[1]
    item_id = callback.data.split("_")[2]
    
    await callback.answer("❌ Действие отменено")
    await callback.message.edit_text(
        f"❌ Действие отменено.\n\n"
        "Возвращаемся к списку привычек."
    )


# Обработчики для напоминаний
@callback_router.callback_query(F.data.startswith("reminder_done_"))
async def handle_reminder_done(callback: CallbackQuery):
    """Обработчик отметки напоминания как выполненного"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("✅ Привычка отмечена как выполненная!")
    await callback.message.edit_text(
        f"✅ Отлично! Привычка #{habit_id} выполнена!\n\n"
        "Продолжайте в том же духе! 🎉"
    )


@callback_router.callback_query(F.data.startswith("reminder_later_"))
async def handle_reminder_later(callback: CallbackQuery):
    """Обработчик отложенного напоминания"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("⏰ Напоминание отложено на 1 час")
    await callback.message.edit_text(
        f"⏰ Напоминание отложено на 1 час.\n\n"
        "Я напомню вам снова позже."
    )


@callback_router.callback_query(F.data.startswith("reminder_skip_"))
async def handle_reminder_skip(callback: CallbackQuery):
    """Обработчик пропуска напоминания"""
    habit_id = callback.data.split("_")[-1]
    
    await callback.answer("❌ Напоминание пропущено")
    await callback.message.edit_text(
        f"❌ Напоминание пропущено.\n\n"
        "Не расстраивайтесь! Завтра новый день! 💪"
    )
