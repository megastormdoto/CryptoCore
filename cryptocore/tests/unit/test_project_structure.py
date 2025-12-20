#!/usr/bin/env python3
"""
Тест для определения реальной структуры проекта
"""

import os
import sys


def print_project_structure():
    """Печатает структуру проекта"""
    print("=" * 60)
    print("АНАЛИЗ СТРУКТУРЫ ПРОЕКТА")
    print("=" * 60)

    # Текущая директория (где мы запускаем тест)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))

    print(f"Текущая директория: {current_dir}")
    print(f"Корень проекта: {project_root}")
    print()

    # Собираем все Python файлы
    python_files = []
    for root, dirs, files in os.walk(project_root):
        # Пропускаем служебные директории
        if '__pycache__' in root or '.pytest_cache' in root or '.venv' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                rel_path = os.path.relpath(os.path.join(root, file), project_root)
                python_files.append(rel_path)

    # Группируем файлы
    print(f"Всего Python файлов: {len(python_files)}")
    print("\nКлючевые файлы:")

    # Ищем cryptocore.py
    cryptocore_files = [f for f in python_files if 'cryptocore' in f.lower() and f.endswith('.py')]
    print(f"\nФайлы cryptocore: {len(cryptocore_files)}")
    for f in cryptocore_files[:10]:  # первые 10
        print(f"  • {f}")

    # Ищем src/ директорию
    src_files = [f for f in python_files if f.startswith('src') or '\\src\\' in f or '/src/' in f]
    print(f"\nФайлы в src/: {len(src_files)}")
    for f in src_files[:10]:
        print(f"  • {f}")

    # Ищем основные модули
    print("\nПоиск основных модулей:")
    modules_to_find = [
        'cli_parser', 'file_io', 'csprng', 'main',
        'aes', 'sha256', 'sha3_256', 'hmac', 'pbkdf2',
        'ecb', 'cbc', 'cfb', 'ofb', 'ctr', 'gcm'
    ]

    for module in modules_to_find:
        found = [f for f in python_files if module in f.lower()]
        if found:
            print(f"  ✅ {module}: найдено {len(found)} файлов")
            for f in found[:2]:  # первые 2
                print(f"     - {f}")
        else:
            print(f"  ❌ {module}: не найдено")

    return project_root


def check_imports_from_root(project_root):
    """Проверяет импорты из корня проекта"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ИМПОРТОВ")
    print("=" * 60)

    # Добавляем корень проекта в путь
    sys.path.insert(0, project_root)

    # Пробуем импортировать cryptocore.py из корня
    cryptocore_path = None
    for root, dirs, files in os.walk(project_root):
        if 'cryptocore.py' in files:
            cryptocore_path = os.path.join(root, 'cryptocore.py')
            break

    if cryptocore_path:
        print(f"✅ Найден cryptocore.py: {os.path.relpath(cryptocore_path, project_root)}")

        # Пробуем импортировать
        try:
            # Добавляем директорию с cryptocore.py в путь
            cryptocore_dir = os.path.dirname(cryptocore_path)
            sys.path.insert(0, cryptocore_dir)

            import cryptocore
            print("✅ Модуль cryptocore успешно импортирован!")

            # Проверяем содержимое
            if hasattr(cryptocore, 'CryptoCore'):
                print("✅ Найден класс CryptoCore")

            if hasattr(cryptocore, 'main'):
                print("✅ Найдена функция main()")

            if hasattr(cryptocore, 'get_symbol'):
                print("✅ Найдена функция get_symbol()")

            return True
        except ImportError as e:
            print(f"❌ Ошибка импорта cryptocore: {e}")
        except Exception as e:
            print(f"❌ Другая ошибка: {e}")
    else:
        print("❌ Файл cryptocore.py не найден в проекте")

    return False


def check_src_imports(project_root):
    """Проверяет импорты из src директории"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ИМПОРТОВ ИЗ ПОДДИРЕКТОРИЙ")
    print("=" * 60)

    # Ищем src директорию или аналогичную
    possible_dirs = ['src', 'source', 'lib', 'cryptocore', 'modules']

    for dir_name in possible_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ Найдена директория: {dir_name}/")

            # Добавляем в путь
            sys.path.insert(0, dir_path)

            # Смотрим что внутри
            py_files = [f for f in os.listdir(dir_path) if f.endswith('.py')]
            print(f"   Python файлов: {len(py_files)}")

            # Пробуем импортировать основные
            modules_to_try = ['cli_parser', 'file_io', 'csprng', 'main']

            for module in modules_to_try:
                module_path = os.path.join(dir_path, f"{module}.py")
                if os.path.exists(module_path):
                    try:
                        # Динамический импорт
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(module, module_path)
                        module_obj = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module_obj)
                        print(f"   ✅ {module}.py импортирован")
                    except Exception as e:
                        print(f"   ❌ Ошибка импорта {module}.py: {e}")
                else:
                    print(f"   ⚠  {module}.py не найден")

            return True

    print("❌ Не найдено подходящей директории с исходным кодом")
    return False


if __name__ == "__main__":
    project_root = print_project_structure()

    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 60)

    cryptocore_ok = check_imports_from_root(project_root)
    src_ok = check_src_imports(project_root)

    print("\n" + "=" * 60)
    print("РЕКОМЕНДАЦИИ:")
    print("=" * 60)

    if not cryptocore_ok:
        print("1. Убедитесь что cryptocore.py находится в корне проекта")
        print("2. Проверьте наличие __init__.py файлов")

    if not src_ok:
        print("3. Проверьте структуру исходного кода")
        print("4. Возможно код находится прямо в корне, а не в src/")

    print("\nСтруктура проекта должна быть примерно такой:")
    print("cryptocore/")
    print("├── cryptocore.py      # основной файл")
    print("├── cli_parser.py      # или в поддиректории")
    print("├── file_io.py")
    print("├── csprng.py")
    print("├── main.py")
    print("├── modes/")
    print("│   ├── ecb.py")
    print("│   ├── cbc.py")
    print("│   └── ...")
    print("└── tests/")
    print("    └── unit/")
    print("        └── test_*.py")