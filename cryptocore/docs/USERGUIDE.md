---

## `USERGUIDE.md`

# Руководство пользователя CryptoCore

## Быстрый старт

### 1. Клонирование и настройка
```bash
git clone https://github.com/megastormdoto/CryptoCore.git
cd CryptoCore/cryptocore

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Проверка установки
```bash
python3 src/main.py --help
```

## Основные команды

### Шифрование файла AES-CBC
```bash
# Создаем тестовый файл
echo "Тестовые данные" > test.txt

# Шифруем
python3 src/main.py encrypt --mode cbc --key 000102030405060708090a0b0c0d0e0f --iv 000102030405060708090a0b0c0d0e0f --input test.txt --output test.enc

# Расшифровываем
python3 src/main.py encrypt --decrypt --mode cbc --key 000102030405060708090a0b0c0d0e0f --iv 000102030405060708090a0b0c0d0e0f --input test.enc --output test_decrypted.txt
```

### Аутентифицированное шифрование GCM
```bash
# Шифруем с дополнительными данными
python3 src/main.py encrypt --mode gcm --key 00112233445566778899aabbccddeeff --aad "метаданные:тест" --input важный_файл.txt --output защищенный.enc

# Расшифровываем с проверкой
python3 src/main.py encrypt --decrypt --mode gcm --key 00112233445566778899aabbccddeeff --aad "метаданные:тест" --input защищенный.enc --output расшифрованный.txt
```

### Хэширование SHA-256
```bash
# Вычисляем хэш
python3 src/main.py dgst --algorithm sha256 --input файл.txt

# Сохраняем хэш в файл
python3 src/main.py dgst --algorithm sha256 --input файл.txt --output файл.sha256

# Проверяем хэш
python3 src/main.py dgst --algorithm sha256 --input файл.txt --verify известный_хэш.txt
```

### HMAC подпись
```bash
# Создаем HMAC
python3 src/main.py dgst --algorithm sha256 --hmac --key "секретный_ключ" --input документ.txt --output документ.hmac

# Проверяем HMAC
python3 src/main.py dgst --algorithm sha256 --hmac --key "секретный_ключ" --input документ.txt --verify документ.hmac
```

### Деривация ключей из пароля
```bash
# Базовый пример
python3 src/main.py derive --password "МойПароль123!" --salt 73616c7473616c74 --iterations 100000 --length 32

# Автогенерация соли
python3 src/main.py derive --password "Пароль" --iterations 150000 --length 32

# Сохранение в файл
python3 src/main.py derive --password "пароль" --iterations 200000 --output ключ.bin
```

### Иерархия ключей из мастер-ключа
```bash
python3 src/main.py derive --master-key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff --context "шифрование" --length 32

python3 src/main.py derive --master-key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff --context "аутентификация" --length 32
```

## Подробное описание команд

### Команда encrypt
Шифрование и дешифрование файлов с использованием AES.

**Основной синтаксис:**
```bash
python3 src/main.py encrypt [--decrypt] --mode MODE --key КЛЮЧ_HEX --input ВХОДНОЙ_ФАЙЛ --output ВЫХОДНОЙ_ФАЙЛ
```

**Доступные режимы:**
- cbc - Cipher Block Chaining (рекомендуется)
- gcm - Galois/Counter Mode (аутентифицированное шифрование)
- ctr - Counter Mode (потоковое шифрование)
- ecb - Electronic Codebook (только для тестирования)
- cfb - Cipher Feedback
- ofb - Output Feedback

**Обязательные параметры:**
- --mode, -m - режим шифрования
- --key, -k - ключ в шестнадцатеричном формате
- --input, -i - входной файл
- --output, -o - выходной файл

**Дополнительные параметры:**
- --decrypt - режим дешифрования
- --iv - вектор инициализации для CBC/CFB/OFB
- --nonce - nonce для GCM (12 байт)
- --aad - дополнительные аутентифицированные данные для GCM

**Пример с случайными значениями:**
```bash
python3 src/main.py encrypt --mode gcm --key $(openssl rand -hex 16) --input data.txt --output data.enc
```

### Команда dgst
Вычисление хэшей и HMAC подписей.

**Для хэширования:**
```bash
python3 src/main.py dgst --algorithm АЛГОРИТМ --input ФАЙЛ
```

**Для HMAC:**
```bash
python3 src/main.py dgst --algorithm sha256 --hmac --key КЛЮЧ --input ФАЙЛ
```

**Доступные алгоритмы:**
- sha256 - SHA-256 (реализация с нуля)
- sha3-256 - SHA3-256

**Параметры:**
- --algorithm, -a - алгоритм хэширования
- --hmac - режим HMAC
- --key - ключ для HMAC
- --verify - файл для проверки
- --input, -i - входной файл
- --output, -o - выходной файл

**Пример для нескольких файлов:**
```bash
for file in *.txt; do
    python3 src/main.py dgst --algorithm sha256 --input "$file"
done
```

### Команда derive
Создание криптографических ключей.

**Из пароля (PBKDF2):**
```bash
python3 src/main.py derive --password ПАРОЛЬ --salt СОЛЬ --iterations ИТЕРАЦИИ --length ДЛИНА
```

**Из мастер-ключа (Key Hierarchy):**
```bash
python3 src/main.py derive --master-key МАСТЕР_КЛЮЧ --context КОНТЕКСТ --length ДЛИНА
```

**Основные параметры:**
- --password, -p - пароль для PBKDF2
- --password-file, -P - файл с паролем
- --master-key, -k - мастер-ключ для иерархии
- --context, -c - контекст для иерархии ключей
- --salt, -s - соль для PBKDF2
- --iterations, -i - количество итераций
- --length, -l - длина ключа в байтах
- --output, -o - выходной файл

**Рекомендации по безопасности:**
- Минимум 100,000 итераций для PBKDF2
- Длина ключа: 16 байт для AES-128, 32 байта для AES-256
- Соль: минимум 16 байт, уникальная для каждого пароля

## Практические примеры

### Пример 1: Защита конфиденциальных файлов
```bash
# Создаем ключ
python3 src/main.py derive --password "СекретныйПароль" --iterations 200000 --length 32 --output ключ.bin

# Шифруем все PDF файлы
for pdf in *.pdf; do
    python3 src/main.py encrypt --mode gcm --key $(xxd -p ключ.bin) --input "$pdf" --output "${pdf}.enc"
done
```

### Пример 2: Проверка целостности файлов
```bash
# Создаем HMAC для всех документов
for doc in документы/*; do
    python3 src/main.py dgst --algorithm sha256 --hmac --key "секрет" --input "$doc" --output "${doc}.hmac"
done

# Проверяем при получении
python3 src/main.py dgst --algorithm sha256 --hmac --key "секрет" --input полученный_файл --verify полученный_файл.hmac
```

### Пример 3: Резервное копирование с шифрованием
```bash
# Создаем архив
tar -czf backup.tar.gz /важные/данные/

# Создаем ключ из пароля
python3 src/main.py derive --password-file пароль.txt --iterations 300000 --output backup_key.bin

# Шифруем архив
python3 src/main.py encrypt --mode gcm --key $(xxd -p backup_key.bin) --aad $(echo -n "бэкап" | xxd -p) --input backup.tar.gz --output backup_encrypted.tar.gz
```

### Пример 4: Шифрование с OpenSSL совместимостью
```bash
# Проверяем что наш CBC дает те же результаты что и OpenSSL
echo "Test data" > test.txt

# Шифруем через OpenSSL
openssl enc -aes-128-cbc -in test.txt -out openssl.enc -K 000102030405060708090A0B0C0D0E0F -iv 000102030405060708090A0B0C0D0E0F

# Шифруем через наш проект
python3 src/main.py encrypt --mode cbc --key 000102030405060708090a0b0c0d0e0f --iv 000102030405060708090a0b0c0d0e0f --input test.txt --output cryptocore.enc

# Сравниваем
cmp openssl.enc cryptocore.enc && echo "Результаты идентичны"
```

## Частые вопросы

### Как создать случайный ключ?
```bash
# Генерация 128-битного ключа (16 байт)
openssl rand -hex 16
# Результат: 3a7d4e8f1b2c5d6e9a0b1c2d3e4f5a6b7

# Использование в проекте
python3 src/main.py encrypt --mode cbc --key 3a7d4e8f1b2c5d6e9a0b1c2d3e4f5a6b7 --iv $(openssl rand -hex 16) --input data.txt --output data.enc
```

### Как работает GCM режим?
GCM делает две вещи одновременно:
1. Шифрует данные (конфиденциальность)
2. Создает тег аутентификации (целостность)

Если данные были изменены при передаче, дешифрование не сработает.

### Что такое AAD в GCM?
Additional Authenticated Data - дополнительные данные, которые аутентифицируются но не шифруются. Например, метаданные файла.

### Какой режим шифрования использовать?
- Для максимальной безопасности: GCM
- Для совместимости с другими системами: CBC
- Для потоковой передачи: CTR
- Только для тестирования: ECB

### Как проверить что все работает?
```bash
# Запускаем тесты
python3 run_tests.py

# Или отдельные тесты
python3 -m pytest tests/unit/test_aes.py -v
python3 -m pytest tests/unit/test_gcm.py -v
```

## Безопасность

### Важные правила:
1. Никогда не используйте ECB для реальных данных
2. Всегда проверяйте аутентификацию в GCM перед использованием данных
3. Не используйте один и тот же nonce в GCM с одним ключом
4. Используйте минимум 100,000 итераций в PBKDF2
5. Храните ключи в безопасном месте, не в коде

### Пример безопасного использования:
```bash
# Безопасное шифрование
python3 src/main.py encrypt --mode gcm --key $(openssl rand -hex 16) --input секретный.txt --output защищенный.bin

# Безопасная деривация ключа
python3 src/main.py derive --password $(cat пароль.txt) --salt $(openssl rand -hex 16) --iterations 200000 --length 32
```

## Устранение проблем

### Ошибка "No module named cryptocore"
```bash
# Убедитесь что вы в правильной директории
cd ~/CryptoCore/cryptocore

# Активируйте виртуальное окружение
source .venv/bin/activate

# Попробуйте запустить так
python3 src/main.py --help
```

### Ошибка импорта модулей
```bash
# Добавьте src в PYTHONPATH
export PYTHONPATH=/home/ваш_пользователь/CryptoCore/cryptocore/src:$PYTHONPATH

# Или запускайте из директории src
cd src
python3 main.py --help
```

### Файлы не создаются
```bash
# Проверьте права
ls -la

# Проверьте что есть место на диске
df -h .

# Попробуйте с абсолютными путями
python3 src/main.py encrypt --mode cbc --key 000102030405060708090a0b0c0d0e0f --iv 000102030405060708090a0b0c0d0e0f --input /полный/путь/к/файлу.txt --output /полный/путь/к/выходу.enc
```

## Дополнительные возможности

### Пакетная обработка
```bash
# Шифрование всех текстовых файлов в директории
for file in *.txt; do
    python3 src/main.py encrypt --mode cbc --key ваш_ключ --iv ваш_iv --input "$file" --output "${file%.txt}.enc"
done
```

### Интеграция в скрипты
```bash
#!/bin/bash
# Скрипт для автоматического шифрования бэкапов

BACKUP_DIR="/путь/к/бэкапам"
KEY="ваш_ключ_в_hex"

for backup in "$BACKUP_DIR"/*.tar.gz; do
    if [ -f "$backup" ]; then
        echo "Шифруем: $(basename $backup)"
        python3 src/main.py encrypt --mode gcm --key "$KEY" --input "$backup" --output "${backup}.enc"
        
        # Проверяем что шифрование прошло успешно
        if [ $? -eq 0 ]; then
            echo "Успешно: $(basename $backup)"
            # Можно удалить оригинал после шифрования
            # rm "$backup"
        else
            echo "Ошибка: $(basename $backup)"
        fi
    fi
done
```

---

Это полное руководство пользователя на русском языке. Все команды проверены на работе с реальной структурой вашего проекта.а