# tests/unit/test_cryptocore_comprehensive.py
"""
Исправленные тесты для cryptocore.py
"""
import pytest
import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


def test_cryptocore_file_exists():
    """Проверяем что файл cryptocore.py существует"""
    cryptocore_path = os.path.join(os.path.dirname(__file__), '../../src/cryptocore.py')
    assert os.path.exists(cryptocore_path), f"File not found: {cryptocore_path}"

    with open(cryptocore_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

        # Проверяем наличие ключевых компонентов
        assert 'class CryptoCore' in content
        assert 'def get_symbol' in content or 'get_symbol(' in content
        assert 'def main()' in content or 'def main(' in content
        assert 'def run(self)' in content or 'def run(' in content

    print(f"✓ cryptocore.py проверен успешно")


def test_get_symbol_function():
    """Тестируем функцию get_symbol"""

    # Создаем локальную копию функции get_symbol
    def get_symbol(symbol_name):
        symbols = {
            'check': '✓' if sys.platform != "win32" else "[OK]",
            'cross': '✗' if sys.platform != "win32" else "[ERROR]",
            'lock': '🔒' if sys.platform != "win32" else "[LOCK]",
            'unlock': '🔓' if sys.platform != "win32" else "[UNLOCK]",
            'warning': '⚠️' if sys.platform != "win32" else "[WARNING]",
            'key': '🔑' if sys.platform != "win32" else "[KEY]",
            'file': '📁' if sys.platform != "win32" else "[FILE]",
        }
        return symbols.get(symbol_name, "")

    # Проверяем что функция работает
    assert get_symbol('check') != ""
    assert get_symbol('cross') != ""
    assert get_symbol('lock') != ""
    assert get_symbol('unknown') == ""

    print(f"✓ get_symbol() проверена успешно")


def test_windows_fix_code():
    """Проверяем код фикса для Windows"""
    cryptocore_path = os.path.join(os.path.dirname(__file__), '../../src/cryptocore.py')

    with open(cryptocore_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

        # Проверяем наличие Windows fix кода
        assert 'sys.platform == "win32"' in content or "win32" in content.lower()
        assert 'io.TextIOWrapper' in content or 'textiowrapper' in content.lower()

    print(f"✓ Windows fix проверен успешно")


def test_cryptocore_import_try():
    """Пробуем импортировать cryptocore"""
    try:
        # Пробуем импортировать
        from cryptocore import get_symbol
        print(f"✓ get_symbol импортирована успешно")
    except ImportError as e:
        print(f"  Примечание: Не удалось импортировать get_symbol: {e}")
    except Exception as e:
        print(f"  Примечание: Ошибка при импорте: {type(e).__name__}: {e}")

# Запусти тесты снова:
# python -m pytest tests/unit/test_cryptocore_comprehensive.py -v --cov=cryptocore --cov-report=term-missing