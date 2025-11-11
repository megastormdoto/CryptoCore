## CryptoCore
Командная утилита для шифрования, дешифрования и хеширования файлов с использованием AES-128 в различных режимах работы и криптографических хеш-функций.


# CryptoCore - Cryptographic Core Operations

Инструмент командной строки для шифрования и дешифрования с использованием AES-128 в различных режимах работы.

## Установка
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

## Использование

### Основные режимы работы:

- **ECB** (Electronic Codebook) - базовый режим без обратной связи
- **CBC** (Cipher Block Chaining) - режим сцепления блоков шифротекста  
- **CFB** (Cipher Feedback) - режим обратной связи по шифротексту
- **OFB** (Output Feedback) - режим обратной связи по выходу
- **CTR** (Counter) - режим счетчика

### Примеры использования:

**Шифрование файла в режиме ECB:**
```bash
python main.py --algorithm aes --mode ecb --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test.txt --output encrypted.bin
```

**Дешифрование файла в режиме ECB:**
```bash
python main.py --algorithm aes --mode ecb --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input encrypted.bin --output decrypted.txt
```

**Шифрование в режиме CBC (IV генерируется автоматически):**
```bash
python main.py --algorithm aes --mode cbc --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input document.txt --output encrypted.bin
```

**Дешифрование в режиме CBC (IV читается из файла):**
```bash
python main.py --algorithm aes --mode cbc --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input encrypted.bin --output decrypted.txt
```

**Дешифрование с указанием IV:**
```bash
python main.py --algorithm aes --mode cbc --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --iv AABBCCDDEEFF00112233445566778899 \
    --input ciphertext.bin --output decrypted.txt
```

**Режим CTR с указанием счетчика:**
```bash
python main.py --algorithm aes --mode ctr --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input data.txt --output encrypted.bin
```

## Параметры командной строки

| Параметр | Обязательный | Описание |
|----------|--------------|----------|
| `--algorithm`, `-a` | ✅ | Алгоритм шифрования (`aes`) |
| `--mode`, `-m` | ✅ | Режим работы (`ecb`, `cbc`, `cfb`, `ofb`, `ctr`) |
| `--encrypt`, `-e` | ✅ | Режим шифрования |
| `--decrypt`, `-d` | ✅ | Режим дешифрования |
| `--key`, `-k` | ✅ | Ключ в HEX-формате (32 символа, 16 байт) |
| `--input`, `-i` | ✅ | Входной файл |
| `--output`, `-o` | ❌ | Выходной файл (опционально) |
| `--iv` | ❌ | Вектор инициализации в HEX-формате (только для дешифрования) |

## Формат ключа и IV

**Ключ:** 32-символьная HEX-строка (16 байт для AES-128)
```
00112233445566778899aabbccddeeff
```

**IV:** 32-символьная HEX-строка (16 байт)
```
AABBCCDDEEFF00112233445566778899
```

## Особенности реализации

### Обработка IV:
- **Шифрование:** IV генерируется автоматически и сохраняется в начале выходного файла
- **Дешифрование:** 
  - Если `--iv` указан, используется предоставленный вектор
  - Если `--iv` не указан, IV читается из первых 16 байт входного файла

### Паддинг:
- **С паддингом:** ECB, CBC (используют PKCS#7)
- **Без паддинга:** CFB, OFB, CTR (потоковые режимы)

### Структура зашифрованных файлов:
```
Для ECB: [зашифрованные данные]
Для CBC/CFB/OFB: [16 байт IV][зашифрованные данные]
Для CTR: [зашифрованные данные] (счетчик используется как IV)
```

## OpenSSL Совместимость

CryptoCore полностью совместим с OpenSSL для всех режимов работы.

### Тестирование совместимости с OpenSSL:

**1. Шифрование CryptoCore → Дешифрование OpenSSL:**
```bash
# Шифруем файл с помощью CryptoCore
python main.py --algorithm aes --mode cbc --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input plain.txt --output cipher.bin

# Извлекаем IV из зашифрованного файла
dd if=cipher.bin of=iv.bin bs=16 count=1
dd if=cipher.bin of=ciphertext_only.bin bs=16 skip=1

# Дешифруем с помощью OpenSSL
openssl enc -aes-128-cbc -d \
    -K 00112233445566778899aabbccddeeff \
    -iv $(xxd -p iv.bin | tr -d '\n') \
    -in ciphertext_only.bin -out decrypted_openssl.txt
```

**2. Шифрование OpenSSL → Дешифрование CryptoCore:**
```bash
# Шифруем файл с помощью OpenSSL
openssl enc -aes-128-cbc \
    -K 00112233445566778899aabbccddeeff \
    -iv AABBCCDDEEFF00112233445566778899 \
    -in plain.txt -out openssl_cipher.bin

# Дешифруем с помощью CryptoCore
python main.py --algorithm aes --mode cbc --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --iv AABBCCDDEEFF00112233445566778899 \
    --input openssl_cipher.bin --output decrypted_cryptocore.txt
```

### Запуск тестов совместимости:
```bash
python test_openssl_compatibility.py
```

## Пример полного цикла
```bash
# Шифруем тестовый файл в режиме CBC
python main.py --algorithm aes --mode cbc --encrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test.txt --output test_encrypted.bin

# Дешифруем обратно
python main.py --algorithm aes --mode cbc --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input test_encrypted.bin --output test_decrypted.txt

# Проверяем результат
python -c "print('SUCCESS!' if open('test.txt').read() == open('test_decrypted.txt').read() else 'FAILED')"
```

## Тестирование

```bash
# Запуск всех тестов
python test_full.py

# Тестирование отдельных режимов
python test_ecb_all.py
python test_all_modes.py

# Тестирование CLI
python test_cli.py

# Тестирование ввода/вывода
python test_io.py

# Тест совместимости с OpenSSL
python test_openssl_compatibility.py
```

## Структура проекта

```
cryptocore/
├── .venv/                     # Виртуальное окружение
├── src/                       # Исходный код
│   ├── modes/                 # Реализации режимов шифрования
│   │   ├── __init__.py       # Базовый класс режимов
│   │   ├── ecb.py            # Реализация режима ECB
│   │   ├── cbc.py            # Реализация режима CBC
│   │   ├── cfb.py            # Реализация режима CFB
│   │   ├── ofb.py            # Реализация режима OFB
│   │   └── ctr.py            # Реализация режима CTR
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
│   ├── test_all_modes.py     # Тесты всех режимов
│   ├── test_openssl_compatibility.py  # Тесты совместимости
│   └── test_plain.txt        # Тестовые данные
├── requirements.txt           # Зависимости проекта
├── main.py                   # Точка входа
└── README.md                 # Документация
```

## Технические детали

- **Алгоритм:** AES-128
- **Режимы:** ECB, CBC, CFB, OFB, CTR
- **Паддинг:** PKCS#7 (для ECB и CBC)
- **Формат ключа:** HEX-строка (32 символа)
- **Генерация IV:** os.urandom(16)
- **Библиотека:** pycryptodome

## Зависимости

Основная зависимость - `pycryptodome` для криптографических операций.

```bash
pip install pycryptodome
```

## Рекомендации по безопасности

-  **Рекомендуется:** CBC, CTR, CFB, OFB
-  **С осторожностью:** ECB (только для тестирования)
-  **Обязательно:** Используйте случайные IV для CBC/CFB/OFB
-  **Хранение:** Сохраняйте IV вместе с зашифрованными данными
-  **Не используйте ECB** для защиты чувствительных данных

## Отладка

Если возникают проблемы:
1. Проверьте формат ключа (ровно 32 HEX-символа)
2. Убедитесь что входной файл существует
3. Для дешифрования убедитесь, что IV корректен или присутствует в файле
4. Запустите тесты для проверки работоспособности
5. Проверьте совместимость с OpenSSL используя тестовые скрипты

## Важные заметки

- Всегда делайте бэкап важных файлов перед шифрованием
- Храните ключи в безопасном месте
- Используйте тестовые файлы для проверки работы
- Режим ECB не рекомендуется для защиты чувствительных данных

---

## Новые возможности (Sprint 2)

### Реализованные режимы:
-  **CBC** (Cipher Block Chaining) - с цепочкой блоков
-  **CFB** (Cipher Feedback) - режим обратной связи  
-  **OFB** (Output Feedback) - режим выходной обратной связи
-  **CTR** (Counter) - режим счетчика

### Ключевые улучшения:
- Полная совместимость с OpenSSL
- Автоматическая генерация и управление IV
- Поддержка потоковых режимов без паддинга
- Расширенная валидация параметров CLI
- Комплексное тестирование всех режимов

### Статус реализации:
Все требования Sprint 2 успешно выполнены, включая:
- Реализацию 4 новых режимов работы
- Корректную обработку IV
- Совместимость с OpenSSL
- Комплексное тестирование
```

Основные улучшения в обновленном README:

1. **Полная документация по новым режимам** - CBC, CFB, OFB, CTR
2. **Подробные примеры использования** с IV и без
3. **Инструкции по совместимости с OpenSSL** с конкретными командами
4. **Обновленная структура параметров CLI** с новыми опциями
5. **Технические детали реализации** - паддинг, обработка IV, структура файлов
6. **Рекомендации по безопасности** для каждого режима
7. **Раздел "Новые возможности"** с итогами Sprint 2
8. **Улучшенная навигация** и структура документа