import unittest
from datetime import datetime

class TestWeatherDiary(unittest.TestCase):
    
    def test_date_format(self):
        """Проверка формата даты"""
        def validate_date(date_str):
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        
        self.assertTrue(validate_date("2026-05-04"))
        self.assertTrue(validate_date("2024-12-31"))
        self.assertTrue(validate_date("2025-01-01"))
        self.assertFalse(validate_date("04.05.2026"))
        self.assertFalse(validate_date("2026/05/04"))
        self.assertFalse(validate_date("2026-13-04"))
        self.assertFalse(validate_date("2026-05-32"))
    
    def test_temperature_conversion(self):
        """Проверка преобразования температуры"""
        def validate_temp(temp_str):
            try:
                float(temp_str)
                return True
            except ValueError:
                return False
        
        self.assertTrue(validate_temp("15"))
        self.assertTrue(validate_temp("-5"))
        self.assertTrue(validate_temp("-5.5"))
        self.assertTrue(validate_temp("0"))
        self.assertTrue(validate_temp("99.9"))
        self.assertFalse(validate_temp("abc"))
        self.assertFalse(validate_temp("15d"))
        self.assertFalse(validate_temp(""))
    
    def test_empty_description(self):
        """Проверка описания (не должно быть пустым)"""
        def is_valid_description(desc):
            return bool(desc and desc.strip())
        
        self.assertTrue(is_valid_description("Солнечно"))
        self.assertTrue(is_valid_description("  Дождь  "))
        self.assertFalse(is_valid_description(""))
        self.assertFalse(is_valid_description("   "))
    
    def test_precipitation_format(self):
        """Проверка формата осадков (только Да или Нет)"""
        def format_precipitation(value):
            return "Да" if value else "Нет"
        
        self.assertEqual(format_precipitation(True), "Да")
        self.assertEqual(format_precipitation(False), "Нет")
        self.assertIn(format_precipitation(True), ["Да", "Нет"])
        self.assertIn(format_precipitation(False), ["Да", "Нет"])
    
    def test_temperature_range(self):
        """Проверка фильтрации по диапазону температур"""
        entries = [
            {"temperature": -5},
            {"temperature": 0},
            {"temperature": 10},
            {"temperature": 15},
            {"temperature": 25},
        ]
        
        def filter_by_temp(entries, min_temp=None, max_temp=None):
            result = entries
            if min_temp is not None:
                result = [e for e in result if e["temperature"] >= min_temp]
            if max_temp is not None:
                result = [e for e in result if e["temperature"] <= max_temp]
            return result
        
        # Только минимум
        result = filter_by_temp(entries, min_temp=10)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["temperature"], 10)
        
        # Только максимум
        result = filter_by_temp(entries, max_temp=10)
        self.assertEqual(len(result), 3)
        
        # Диапазон
        result = filter_by_temp(entries, min_temp=0, max_temp=15)
        self.assertEqual(len(result), 3)
        
        # Пустой диапазон
        result = filter_by_temp(entries, min_temp=30, max_temp=40)
        self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()
