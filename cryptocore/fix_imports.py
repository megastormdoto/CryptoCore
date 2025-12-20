#!/usr/bin/env python3
"""
Скрипт для исправления импортов в тестах
"""

import os
import re


def fix_test_file(filepath):
    """Исправляет импорты в тестовом файле"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Проверяем есть ли проблемные импорты
    if 'import cryptocore' in content or 'from cryptocore import' in content:
        print(f"Исправляю {filepath}")

        # Добавляем правильные пути импорта в начало
        fix_code = '''import sys
import os
# Добавляем src в путь для правильного импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
'''

        # Если уже есть импорт sys/os, не добавляем дубли
        if 'import sys' not in content or 'import os' not in content:
            content = fix_code + content

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# Файлы которые нужно исправить
test_files = [
    'tests/unit/test_cryptocore_simple.py',
    'tests/unit/test_real_coverage.py',
    'tests/unit/test_pbkdf2_comprehensive.py',
]

for test_file in test_files:
    if os.path.exists(test_file):
        fix_test_file(test_file)
        print(f"✅ Исправлен: {test_file}")
    else:
        print(f"⚠  Не найден: {test_file}")

print("\n✅ Готово! Теперь запусти тесты снова.")