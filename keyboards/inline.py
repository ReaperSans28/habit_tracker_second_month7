"""
Inline клавиатуры
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_habit_actions_keyboard(habit_id: int = None):
    """Создает клавиатуру действий с привычкой"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Выполнено", callback_data=f"habit_done_{habit_id}"),
                InlineKeyboardButton(text="❌ Пропущено", callback_data=f"habit_skip_{habit_id}")
            ],
            [
                InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"habit_edit_{habit_id}"),
                InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"habit_delete_{habit_id}")
            ],
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data=f"habit_stats_{habit_id}")
            ]
        ]
    )
    return keyboard


def get_confirmation_keyboard(action: str, item_id: int = None):
    """Создает клавиатуру подтверждения действия"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data=f"confirm_{action}_{item_id}"),
                InlineKeyboardButton(text="❌ Нет", callback_data=f"cancel_{action}_{item_id}")
            ]
        ]
    )
    return keyboard


def get_habit_list_keyboard(habits: list = None):
    """Создает клавиатуру списка привычек"""
    if not habits:
        habits = ["Пример привычки 1", "Пример привычки 2"]
    
    keyboard_buttons = []
    for i, habit in enumerate(habits):
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"📝 {habit}", 
                callback_data=f"select_habit_{i}"
            )
        ])
    
    # Добавляем кнопку "Добавить новую привычку"
    keyboard_buttons.append([
        InlineKeyboardButton(text="➕ Добавить новую привычку", callback_data="add_new_habit")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard
