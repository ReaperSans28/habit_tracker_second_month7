"""
Модуль для интеграции с календарем
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import calendar


class CalendarIntegration:
    """Класс для работы с календарными функциями"""
    
    def __init__(self):
        self.weekdays = {
            'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3,
            'пятница': 4, 'суббота': 5, 'воскресенье': 6
        }
    
    def get_week_schedule(self, start_date: datetime, frequency: Dict) -> List[datetime]:
        """
        Генерирует расписание на неделю
        """
        if not frequency:
            return []
        
        schedule = []
        current_date = start_date
        
        if frequency['type'] == 'daily':
            for i in range(7):
                if i % frequency['interval'] == 0:
                    schedule.append(current_date)
                current_date += timedelta(days=1)
        
        elif frequency['type'] == 'weekly':
            # Находим нужный день недели
            target_weekday = self._get_target_weekday(frequency)
            days_ahead = target_weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            
            first_occurrence = start_date + timedelta(days=days_ahead)
            schedule.append(first_occurrence)
        
        return schedule
    
    def get_month_schedule(self, start_date: datetime, frequency: Dict) -> List[datetime]:
        """
        Генерирует расписание на месяц
        """
        if not frequency:
            return []
        
        schedule = []
        current_date = start_date
        
        if frequency['type'] == 'daily':
            for i in range(30):  # Примерно месяц
                if i % frequency['interval'] == 0:
                    schedule.append(current_date)
                current_date += timedelta(days=1)
        
        elif frequency['type'] == 'weekly':
            # Находим нужный день недели
            target_weekday = self._get_target_weekday(frequency)
            days_ahead = target_weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            
            first_occurrence = start_date + timedelta(days=days_ahead)
            
            # Добавляем все вхождения в течение месяца
            for week in range(4):
                occurrence = first_occurrence + timedelta(weeks=week)
                if occurrence.month == start_date.month:
                    schedule.append(occurrence)
        
        elif frequency['type'] == 'monthly':
            # Ежемесячно в тот же день
            for month in range(12):
                try:
                    occurrence = start_date.replace(month=start_date.month + month)
                    schedule.append(occurrence)
                except ValueError:
                    # Обработка случая, когда в месяце нет такого дня
                    pass
        
        return schedule
    
    def _get_target_weekday(self, frequency: Dict) -> int:
        """Получает целевой день недели для еженедельных привычек"""
        # По умолчанию - понедельник
        return 0
    
    def get_next_occurrence(self, last_date: datetime, frequency: Dict) -> Optional[datetime]:
        """
        Получает следующее вхождение привычки
        """
        if not frequency:
            return None
        
        if frequency['type'] == 'daily':
            return last_date + timedelta(days=frequency['interval'])
        
        elif frequency['type'] == 'weekly':
            return last_date + timedelta(weeks=frequency['interval'])
        
        elif frequency['type'] == 'monthly':
            # Простое добавление месяца
            year = last_date.year + (last_date.month + frequency['interval'] - 1) // 12
            month = (last_date.month + frequency['interval'] - 1) % 12 + 1
            day = min(last_date.day, calendar.monthrange(year, month)[1])
            return datetime(year, month, day)
        
        return None
    
    def is_habit_due(self, habit_data: Dict, current_time: datetime = None) -> bool:
        """
        Проверяет, пора ли выполнять привычку
        """
        if current_time is None:
            current_time = datetime.now()
        
        if not habit_data.get('frequency'):
            return False
        
        frequency = habit_data['frequency']
        last_completion = habit_data.get('last_completion')
        
        if not last_completion:
            return True
        
        next_occurrence = self.get_next_occurrence(last_completion, frequency)
        if not next_occurrence:
            return False
        
        return current_time >= next_occurrence
    
    def get_habit_stats(self, habit_data: Dict, period_days: int = 30) -> Dict:
        """
        Получает статистику привычки за период
        """
        if not habit_data.get('completions'):
            return {
                'total_completions': 0,
                'completion_rate': 0.0,
                'streak': 0,
                'longest_streak': 0
            }
        
        completions = habit_data['completions']
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Фильтруем завершения за период
        period_completions = [
            comp for comp in completions 
            if comp >= start_date
        ]
        
        total_completions = len(period_completions)
        
        # Вычисляем процент выполнения
        if habit_data.get('frequency'):
            expected_completions = self._calculate_expected_completions(
                habit_data['frequency'], period_days
            )
            completion_rate = (total_completions / expected_completions * 100) if expected_completions > 0 else 0
        else:
            completion_rate = 0
        
        # Вычисляем текущую серию
        streak = self._calculate_current_streak(completions)
        
        # Вычисляем самую длинную серию
        longest_streak = self._calculate_longest_streak(completions)
        
        return {
            'total_completions': total_completions,
            'completion_rate': round(completion_rate, 1),
            'streak': streak,
            'longest_streak': longest_streak
        }
    
    def _calculate_expected_completions(self, frequency: Dict, period_days: int) -> int:
        """Вычисляет ожидаемое количество выполнений за период"""
        if frequency['type'] == 'daily':
            return period_days // frequency['interval']
        elif frequency['type'] == 'weekly':
            return (period_days // 7) * frequency['interval']
        elif frequency['type'] == 'monthly':
            return period_days // 30 * frequency['interval']
        return 0
    
    def _calculate_current_streak(self, completions: List[datetime]) -> int:
        """Вычисляет текущую серию выполнений"""
        if not completions:
            return 0
        
        # Сортируем по убыванию
        sorted_completions = sorted(completions, reverse=True)
        streak = 0
        current_date = datetime.now().date()
        
        for completion in sorted_completions:
            completion_date = completion.date()
            if completion_date == current_date or completion_date == current_date - timedelta(days=1):
                streak += 1
                current_date = completion_date
            else:
                break
        
        return streak
    
    def _calculate_longest_streak(self, completions: List[datetime]) -> int:
        """Вычисляет самую длинную серию выполнений"""
        if not completions:
            return 0
        
        # Сортируем по возрастанию
        sorted_completions = sorted(completions)
        longest_streak = 0
        current_streak = 1
        
        for i in range(1, len(sorted_completions)):
            prev_date = sorted_completions[i-1].date()
            curr_date = sorted_completions[i].date()
            
            if (curr_date - prev_date).days == 1:
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1
        
        return max(longest_streak, current_streak)


# Создаем глобальный экземпляр
calendar_integration = CalendarIntegration()
