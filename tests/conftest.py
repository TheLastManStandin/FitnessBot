"""
Конфигурация pytest для проекта FitnessBot
"""
import os
import sys
from unittest.mock import patch

# Добавляем src в путь Python для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# def pytest_configure(config):
#     """Конфигурация pytest"""
#     # Настройки для тестов
#     config.addinivalue_line(
#         "markers", "integration: mark test as integration test"
#     )
#     config.addinivalue_line(
#         "markers", "unit: mark test as unit test"
#     )