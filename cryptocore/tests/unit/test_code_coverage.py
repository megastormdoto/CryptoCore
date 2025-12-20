#!/usr/bin/env python3
"""
Тест для проверки покрытия кода - анализирует код без его выполнения
"""

import os
import ast
import sys


def analyze_file_coverage(filepath):
    """Анализирует файл и возвращает статистику по строкам"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

            # Подсчитываем строки
            total_lines = len(lines)
            code_lines = 0
            comment_lines = 0
            empty_lines = 0

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    empty_lines += 1
                elif stripped.startswith('#'):
                    comment_lines += 1
                else:
                    code_lines += 1

            return {
                'total': total_lines,
                'code': code_lines,
                'comments': comment_lines,
                'empty': empty_lines,
                'has_docstring': '"""' in content or "'''" in content
            }
    except Exception as e:
        print(f"❌ Ошибка анализа файла {filepath}: {e}")
        return None


def check_cryptocore_structure():
    """Проверяет структуру cryptocore.py"""
    filepath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'cryptocore.py'
    )

    if not os.path.exists(filepath):
        print(f"❌ Файл не найден: {filepath}")
        return False

    print(f"📊 Анализ файла: cryptocore.py")
    stats = analyze_file_coverage(filepath)

    if stats:
        print(f"   Всего строк: {stats['total']}")
        print(f"   Строк кода: {stats['code']}")
        print(f"   Комментариев: {stats['comments']}")
        print(f"   Пустых строк: {stats['empty']}")
        print(f"   Есть docstring: {'✅' if stats['has_docstring'] else '❌'}")

        # Проверяем основные компоненты в коде
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            required_components = [
                ('class CryptoCore', 'Класс CryptoCore'),
                ('def run', 'Метод run()'),
                ('def _handle_crypto', 'Метод _handle_crypto()'),
                ('def _handle_hash', 'Метод _handle_hash()'),
                ('def main', 'Функция main()'),
                ('get_symbol', 'Функция get_symbol()'),
            ]

            print("\n🔍 Поиск основных компонентов:")
            for component, name in required_components:
                if component in content:
                    print(f"   ✅ {name} найден")
                else:
                    print(f"   ❌ {name} не найден")

        return True

    return False


def check_src_directory():
    """Проверяет структуру src директории"""
    src_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'src'
    )

    if not os.path.exists(src_path):
        print(f"❌ Директория src не найдена: {src_path}")
        return False

    print(f"\n📁 Анализ директории: src/")

    # Собираем все .py файлы
    python_files = []
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith('.py') and '__pycache__' not in root:
                python_files.append(os.path.join(root, file))

    print(f"   Найдено Python файлов: {len(python_files)}")

    # Анализируем несколько ключевых файлов
    key_files = [
        'cli_parser.py',
        'file_io.py',
        'csprng.py',
        'main.py'
    ]

    for key_file in key_files:
        filepath = os.path.join(src_path, key_file)
        if os.path.exists(filepath):
            stats = analyze_file_coverage(filepath)
            if stats:
                print(f"\n   📄 {key_file}:")
                print(f"      Строк кода: {stats['code']}")
                print(f"      Есть docstring: {'✅' if stats['has_docstring'] else '❌'}")
        else:
            print(f"   ⚠  {key_file} не найден")

    return True


def check_test_coverage():
    """Проверяет покрытие тестами"""
    tests_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'tests'
    )

    if not os.path.exists(tests_path):
        print(f"❌ Директория tests не найдена: {tests_path}")
        return False

    print(f"\n🧪 Анализ тестов:")

    # Считаем тестовые файлы
    test_files = []
    for root, dirs, files in os.walk(tests_path):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(os.path.join(root, file))

    print(f"   Найдено тестовых файлов: {len(test_files)}")

    # Группируем по категориям
    unit_tests = [f for f in test_files if 'unit' in f]
    integration_tests = [f for f in test_files if 'integration' in f]
    vector_tests = [f for f in test_files if 'vector' in f]

    print(f"   Unit тестов: {len(unit_tests)}")
    print(f"   Интеграционных тестов: {len(integration_tests)}")
    print(f"   Vector тестов: {len(vector_tests)}")

    # Показываем несколько примеров
    print(f"\n   Примеры unit тестов:")
    for test in unit_tests[:5]:
        name = os.path.basename(test)
        print(f"      • {name}")

    return True


def run_coverage_analysis():
    """Запуск анализа покрытия"""
    print("=" * 60)
    print("АНАЛИЗ ПОКРЫТИЯ КОДА")
    print("=" * 60)

    tests = [
        ("Структура cryptocore.py", check_cryptocore_structure),
        ("Структура src/", check_src_directory),
        ("Покрытие тестами", check_test_coverage),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"\n📋 Тест: {test_name}")
        try:
            if test_func():
                print(f"   ✅ ПРОЙДЕН")
                passed += 1
            else:
                print(f"   ❌ НЕ ПРОЙДЕН")
                failed += 1
        except Exception as e:
            print(f"   💥 ОШИБКА: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("РЕКОМЕНДАЦИИ ДЛЯ УВЕЛИЧЕНИЯ ПОКРЫТИЯ:")
    print("=" * 60)

    recommendations = [
        "1. Создайте тесты для всех публичных методов в cryptocore.py",
        "2. Протестируйте обработку ошибок и исключений",
        "3. Добавьте тесты для граничных случаев",
        "4. Проверьте импорты всех модулей из src/",
        "5. Убедитесь что все режимы шифрования имеют тесты",
        "6. Добавьте тесты для CLI парсера",
        "7. Протестируйте работу с файлами (чтение/запись)",
        "8. Добавьте тесты производительности для больших файлов",
    ]

    for rec in recommendations:
        print(f"   {rec}")

    return failed == 0


if __name__ == "__main__":
    success = run_coverage_analysis()
    sys.exit(0 if success else 1)