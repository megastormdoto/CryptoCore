## CryptoCore
Командная утилита для шифрования, дешифрования и хеширования файлов с использованием AES-128 в различных режимах работы и криптографических хеш-функций.

```markdown
# CryptoCore - Cryptographic Core Operations

Инструмент командной строки для шифрования и дешифрования с использованием AES-128 в режиме ECB.

##  Установка

```bash
# Активация виртуального окружения (если используется)
# source .venv/bin/activate  # для Linux/Mac
# .venv\Scripts\activate     # для Windows

# Установка зависимостей
pip install -r requirements.txt
```


## Инструкция для установки

### 1. Скачивание проекта
```bash
git clone https://github.com/megastormdoto/CryptoCore
cd CryptoCore
```

### 2. Установка зависимостей

**Для Windows:**
```cmd
build.bat
```

**Для Linux/macOS:**
```bash
make build
```

**Или вручную:**
```bash
pip install -r requirements.txt
```

### 3. Активация виртуального окружения (рекомендуется)
```cmd
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 4. Использование

**Шифрование файла:**
```bash
python main.py --algorithm aes --mode ecb --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test.txt --output encrypted.bin
```

**Дешифрование файла:**
```bash
python main.py --algorithm aes --mode ecb --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input encrypted.bin --output decrypted.txt
```

### 5. Проверка работы
```bash
# Запуск тестов
python test_ecb_all.py
python test_cli.py
```

## Пример полного цикла
```bash
# Шифруем тестовый файл
python main.py --algorithm aes --mode ecb --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test.txt --output test_encrypted.bin

# Дешифруем обратно
python main.py --algorithm aes --mode ecb --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test_encrypted.bin --output test_decrypted.txt

# Проверяем результат
python -c "print('SUCCESS!' if open('test.txt').read() == open('test_decrypted.txt').read() else 'FAILED')"
```

##  Параметры командной строки
- `--algorithm`: Алгоритм шифрования (только `aes`)
- `--mode`: Режим работы (только `ecb`)
- `--encrypt/--decrypt`: Режим шифрования/дешифрования
- `--key`: Ключ в HEX-формате (32 символа)
- `--input`: Входной файл
- `--output`: Выходной файл (опционально)


##  Использование

### Основной способ (из корня проекта):
```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test_plain.txt --output test_encrypted.bin
```

### Альтернативный способ (если нужен прямой вызов):
```bash
python -m cryptocore.cryptocore --algorithm aes --mode ecb --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test_encrypted.bin --output test_decrypted.txt
```

##  Параметры командной строки

| Параметр | Обязательный | Описание |
|----------|--------------|----------|
| `--algorithm`, `-a` | ✅ | Алгоритм шифрования (`aes`) |
| `--mode`, `-m` | ✅ | Режим работы (`ecb`) |
| `--encrypt`, `-e` | ✅ | Режим шифрования |
| `--decrypt`, `-d` | ✅ | Режим дешифрования |
| `--key`, `-k` | ✅ | Ключ в HEX-формате (32 символа, 16 байт) |
| `--input`, `-i` | ✅ | Входной файл |
| `--output`, `-o` | ❌ | Выходной файл (опционально) |

##  Формат ключа

Ключ должен быть 32-символьной HEX-строкой (16 байт для AES-128):

**Пример правильного ключа:**
```
00112233445566778899aabbccddeeff
```

##  Пример работы

```bash
# Шифруем тестовый файл
python cryptocore.py --algorithm aes --mode ecb --encrypt \
    --key 000102030405060708090a0b0c0d0e0f \
    --input test_plain.txt --output test_encrypted.bin

# Дешифруем обратно
python cryptocore.py --algorithm aes --mode ecb --decrypt \
    --key 000102030405060708090a0b0c0d0e0f \
    --input test_encrypted.bin --output test_decrypted.txt

# Проверяем результат
diff test_plain.txt test_decrypted.txt
```

## Структура проекта

```
cryptocore/
├── .venv/                     # Виртуальное окружение
├── src/                       # Исходный код
│   ├── modes/                 # Реализации режимов шифрования
│   │   └── ecb.py            # Реализация режима ECB
│   ├── __init__.py
│   ├── cli_parser.py         # Парсер аргументов командной строки
│   ├── cryptocore.py         # Главный модуль
│   └── file_io.py            # Утилиты для работы с файлами
├── tests/                     # Тесты
│   ├── __init__.py
│   ├── test_ecb_all.py       # Тесты ECB режима
│   ├── test_cli.py           # Тесты CLI
│   ├── test_full.py          # Полные тесты
│   ├── test_io.py            # Тесты ввода/вывода
│   └── test_plain.txt        # Тестовые данные
├── requirements.txt           # Зависимости проекта
├── cryptocore.py             # Точка входа (возможно)
└── README.md                 # Документация
```

##  Тестирование

```bash
# Запуск всех тестов
python test_full.py

# Тестирование только ECB режима
python test_ecb_all.py

# Тестирование CLI
python test_cli.py

# Тестирование ввода/вывода
python test_io.py
```

##  Тестовые файлы

В проекте есть готовые тестовые файлы:
- `test_plain.txt` - исходный текст
- `test_encrypted.bin` - зашифрованная версия  
- `test_decrypted.txt` - расшифрованная версия
- `final_test.txt`, `final_encrypted.bin`, `final_decrypted.txt` - финальные тесты

##  Технические детали

- **Алгоритм:** AES-128
- **Режим:** ECB (Electronic Codebook)
- **Паддинг:** PKCS#7
- **Формат ключа:** HEX-строка (32 символа)
- **Библиотека:** pycryptodome

##  Зависимости

Основная зависимость - `pycryptodome` для криптографических операций.

```bash
pip install pycryptodome
```

##  Важные заметки

-  **Режим ECB не рекомендуется для защиты чувствительных данных** - используйте только для обучения
-  Всегда делайте бэкап важных файлов перед шифрованием
-  Храните ключи в безопасном месте
-  Используйте тестовые файлы для проверки работы

##  Отладка

Если возникают проблемы:
1. Проверьте формат ключа (ровно 32 HEX-символа)
2. Убедитесь что входной файл существует
3. Запустите тесты для проверки работоспособности

---


1. **Учтена реальная структура** - с виртуальным окружением `.venv` и правильными путями
2. **Правильные пути запуска** - учитывая твою структуру пакетов
3. **Все тестовые файлы** - упомянуты готовые тестовые данные
4. **Конкретные команды тестирования** - под твои тест-файлы
5. **Альтернативные способы запуска** - на случай если нужны разные варианты
