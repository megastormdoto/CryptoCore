# CryptoCore Руководство пользователя

## Содержание
1. [Установка](#установка)
2. [Быстрый старт](#быстрый-старт)
3. [Справочник команд](#справочник-команд)
4. [Примеры](#примеры)
5. [Решение проблем](#решение-проблем)
6. [Рекомендации по безопасности](#рекомендации-по-безопасности)
7. [Частые вопросы](#частые-вопросы)

## Установка

### Требования
- Python 3.8 или новее
- pip (менеджер пакетов Python)

### Способы установки

#### Способ 1: Установка из PyPI (Рекомендуется)
```bash
pip install cryptocore
```

#### Способ 2: Установка из исходного кода
```bash
git clone https://github.com/megastormdoto/CryptoCore
cd CryptoCore
pip install -e .
```

#### Способ 3: Запуск без установки
```bash
python -m cryptocore.cli --help
```

### Проверка установки
```bash
cryptocore --version
cryptocore --help
```

## Быстрый старт

### 1. Создать ключ из пароля
```bash
cryptocore derive --password "МойНадежныйПароль123!" \
    --iterations 100000 --length 32
```

### 2. Зашифровать файл
```bash
cryptocore encrypt --mode gcm \
    --key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff \
    --input секретный.txt \
    --output секретный.enc
```

### 3. Расшифровать файл
```bash
cryptocore encrypt --decrypt --mode gcm \
    --key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff \
    --input секретный.enc \
    --output секретный.dec
```

### 4. Проверить целостность файла
```bash
cryptocore dgst --algorithm sha256 --input секретный.txt

echo "ожидаемый_хэш_здесь" | cryptocore dgst --algorithm sha256 --input секретный.txt --verify -
```

## Справочник команд

### Глобальные опции
Все команды поддерживают эти опции:

- `-h, --help` - Показать справку
- `--version` - Показать версию
- `-v, --verbose` - Подробный вывод
- `--debug` - Режим отладки
- `-q, --quiet` - Только важные сообщения

### Команда: `encrypt` - Шифрование/Расшифровка файлов

Шифрование или расшифровка файлов с использованием AES в различных режимах.

**Базовый синтаксис:**
```bash
cryptocore encrypt [ОПЦИИ]
```

**Опции шифрования:**

| Опция | Обязательно | Описание | По умолчанию |
|--------|----------|-------------|---------|
| `--mode` | Да | Режим шифрования: `ecb`, `cbc`, `cfb`, `ofb`, `ctr`, `gcm` | - |
| `--key` | Да | Ключ шифрования в hex-формате | - |
| `--input, -i` | Да | Входной файл | - |
| `--output, -o` | Да | Выходной файл | - |
| `--decrypt, -d` | Нет | Режим расшифровки | false |
| `--iv` | Для CBC/CFB/OFB | Вектор инициализации в hex | Случайный |
| `--nonce` | Для CTR/GCM | Нонс/счетчик в hex | Случайный |
| `--aad` | Для GCM | Дополнительные аутентифицированные данные в hex | Пусто |
| `--tag` | Расшифровка GCM | Тег аутентификации в hex (если отдельно) | Из файла |

**Размеры ключей:**
- AES-128: 16 байт (32 hex-символа)
- AES-192: 24 байта (48 hex-символов)  
- AES-256: 32 байта (64 hex-символа)

**Примеры:**
```bash
cryptocore encrypt --mode cbc \
    --key 000102030405060708090a0b0c0d0e0f \
    --iv 00112233445566778899aabbccddeeff \
    --input документ.pdf \
    --output документ.enc

cryptocore encrypt --decrypt --mode gcm \
    --key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff \
    --input backup.enc \
    --output backup.tar \
    --aad "backup_2024_03_15"
```

### Команда: `derive` - Генерация ключей

Создание криптографических ключей из паролей или мастер-ключей.

**Базовый синтаксис:**
```bash
cryptocore derive [ОПЦИИ]
```

**Опции:**

| Опция | Обязательно | Описание | По умолчанию |
|--------|----------|-------------|---------|
| `--password, -p` | Одна из опций пароля | Строка пароля | - |
| `--password-file, -P` | Одна из опций пароля | Чтение пароля из файла | - |
| `--password-env, -E` | Одна из опций пароля | Чтение пароля из переменной окружения | - |
| `--master-key, -k` | Альтернатива паролю | Мастер-ключ в hex для иерархии ключей | - |
| `--context, -c` | С master-key | Контекст/назначение ключа | - |
| `--salt, -s` | Нет (авто-генерация) | Соль в hex для PBKDF2 | Случайные 16 байт |
| `--iterations, -i` | Нет | Количество итераций PBKDF2 | 100000 |
| `--length, -l` | Нет | Длина ключа (байты) | 32 |
| `--algorithm, -a` | Нет | Алгоритм: `pbkdf2` или `hkdf` | pbkdf2 |
| `--output, -o` | Нет | Сохранить ключ в бинарный файл | - |
| `--output-salt` | Нет | Сохранить сгенерированную соль в файл | - |
| `--output-key-only` | Нет | Выводить только ключ (без соли) | false |

**Примеры:**
```bash
cryptocore derive --password "МойПароль" \
    --salt a1b2c3d4e5f67890 \
    --iterations 150000 \
    --length 32

echo "СекретныйПароль123!" > pass.txt
cryptocore derive --password-file pass.txt \
    --iterations 200000

cryptocore derive --master-key $(openssl rand -hex 32) \
    --context "шифрование_базы_данных" \
    --length 32

cryptocore derive --password "секрет_приложения" \
    --output ключ_шифрования.bin \
    --output-salt использованная_соль.txt
```

### Команда: `dgst` - Хэш-функции

Вычисление криптографических хэшей файлов.

**Базовый синтаксис:**
```bash
cryptocore dgst [ОПЦИИ]
```

**Опции:**

| Опция | Обязательно | Описание | По умолчанию |
|--------|----------|-------------|---------|
| `--algorithm, -a` | Да | Алгоритм: `sha256`, `sha3-256` | - |
| `--input, -i` | Да | Входной файл | - |
| `--output, -o` | Нет | Выходной файл для хэша | stdout |
| `--verify, -v` | Нет | Проверить соответствие заданному хэшу | - |
| `--check` | Нет | Проверить хэши из файла | - |

**Примеры:**
```bash
cryptocore dgst --algorithm sha256 --input большой_файл.iso

cryptocore dgst --algorithm sha256 \
    --input пакет.zip \
    --verify "a1b2c3d4e5f678901234567890123456789012345678901234567890123456"

echo "a1b2c3...  файл1.txt" > checksums.txt
echo "c3d4e5...  файл2.txt" >> checksums.txt
cryptocore dgst --algorithm sha256 --check checksums.txt
```

### Команда: `hmac` - Коды аутентификации сообщений

Вычисление или проверка HMAC.

**Базовый синтаксис:**
```bash
cryptocore hmac [ОПЦИИ]
```

**Опции:**

| Опция | Обязательно | Описание | По умолчанию |
|--------|----------|-------------|---------|
| `--algorithm, -a` | Нет | Алгоритм хэширования: `sha256`, `sha3-256` | sha256 |
| `--key, -k` | Да | Ключ HMAC | - |
| `--key-file` | Альтернатива | Чтение ключа из файла | - |
| `--input, -i` | Да | Входной файл | - |
| `--verify, -v` | Нет | Проверить соответствие заданному HMAC | - |
| `--output, -o` | Нет | Выходной файл для HMAC | stdout |

**Примеры:**
```bash
cryptocore hmac --key "общий_секрет" \
    --input сообщение.txt \
    --output сообщение.hmac

cryptocore hmac --key "общий_секрет" \
    --input сообщение.txt \
    --verify сообщение.hmac

echo "очень_длинный_секретный_ключ" > hmac_ключ.txt
cryptocore hmac --key-file hmac_ключ.txt \
    --input данные.bin
```

## Примеры

### Полные рабочие процессы

#### 1. Система безопасного резервного копирования
```bash
#!/bin/bash

BACKUP_DIR="/home/user/документы"
ENCRYPTED_DIR="/backup/зашифрованные"
PASSWORD="МастерКлючРезервнойКопии$(date +%Y%m%d)"

tar -czf backup.tar.gz "$BACKUP_DIR"

KEY=$(cryptocore derive --password "$PASSWORD" \
    --iterations 200000 \
    --length 32 \
    --output-key-only)

cryptocore encrypt --mode gcm \
    --key "$KEY" \
    --input backup.tar.gz \
    --output "$ENCRYPTED_DIR/backup_$(date +%Y%m%d).enc" \
    --aad "backup_$(date +%Y%m%d)_$(hostname)"

cryptocore hmac --key "$KEY" \
    --input "$ENCRYPTED_DIR/backup_$(date +%Y%m%d).enc" \
    --output "$ENCRYPTED_DIR/backup_$(date +%Y%m%d).hmac"

echo "Резервная копия зашифрована и проверена"
```

#### 2. Интеграция с менеджером паролей
```bash
#!/bin/bash

read -sp "Пароль базы данных: " DB_PASSWORD
echo

SALT=$(openssl rand -hex 16)
MASTER_KEY=$(openssl rand -hex 32)

ENCRYPTION_KEY=$(cryptocore derive --master-key "$MASTER_KEY" \
    --context "база_данных_prod" \
    --length 32 \
    --output-key-only)

echo "$DB_PASSWORD" > db_pass.txt
cryptocore encrypt --mode gcm \
    --key "$ENCRYPTION_KEY" \
    --input db_pass.txt \
    --output db_pass.enc \
    --aad "production_database"

shred -u db_pass.txt

echo "Пароль зашифрован. Сохраните это безопасно:"
echo "Мастер-ключ: $MASTER_KEY"
echo "Соль: $SALT"
```

#### 3. Мониторинг целостности файлов
```bash
#!/bin/bash

FILES=("/etc/passwd" "/etc/shadow" "/etc/hosts" "/bin/bash")

echo "# Базовые хэши $(date)" > /var/log/целостность_файлов.базовые
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        hash=$(cryptocore dgst --algorithm sha256 --input "$file" --quiet)
        echo "$hash  $file" >> /var/log/целостность_файлов.базовые
    fi
done

echo "Проверка целостности файлов..."
cryptocore dgst --algorithm sha256 \
    --check /var/log/целостность_файлов.базовые
if [ $? -eq 0 ]; then
    echo "Все файлы целы"
else
    echo "ВНИМАНИЕ: Обнаружено изменение файлов!"
fi
```

### Типовые сценарии использования

#### Шифрование конфигурационных файлов
```bash
cryptocore encrypt --mode gcm \
    --key $(cat /etc/cryptocore/ключ.txt) \
    --input конфиг.yaml \
    --output конфиг.yaml.enc \
    --aad "конфиг_приложения_v1"

cryptocore encrypt --decrypt --mode gcm \
    --key $(cat /etc/cryptocore/ключ.txt) \
    --input конфиг.yaml.enc \
    --output /tmp/конфиг.yaml \
    --aad "конфиг_приложения_v1"
```

#### Создание зашифрованного архива
```bash
tar -czf - /var/www/html | \
cryptocore encrypt --mode ctr \
    --key $(openssl rand -hex 32) \
    --output резервная_копия_сайта.enc
```

#### Безопасный обмен сообщениями
```bash
cryptocore encrypt --mode gcm \
    --key $ОБЩИЙ_КЛЮЧ \
    --input сообщение.txt \
    --output сообщение.enc \
    --aad "от:алиса кому:боб $(date)"

cryptocore encrypt --decrypt --mode gcm \
    --key $ОБЩИЙ_КЛЮЧ \
    --input сообщение.enc \
    --output сообщение.txt \
    --aad "от:алиса кому:боб $(date)"
```

## Решение проблем

### Распространенные ошибки

#### "Invalid key length" (Неверная длина ключа)
**Проблема:** Длина ключа не соответствует требованиям.

**Решение:**
```bash
KEY=$(openssl rand -hex 32)
cryptocore encrypt --mode gcm --key "$KEY" --input файл.txt
```

#### "Authentication failed" (Ошибка аутентификации, GCM)
**Проблема:** Не удалось проверить тег аутентификации GCM.

**Причины:**
1. Неправильный ключ
2. Неправильные AAD данные
3. Поврежденный зашифрованный текст
4. Неправильный нонс
5. Файл был изменен

**Решение:**
```bash
cryptocore encrypt --decrypt --mode gcm \
    --key "$ТОТ_ЖЕ_САМЫЙ_КЛЮЧ" \
    --input файл.enc \
    --output файл.dec \
    --aad "$ТЕ_ЖЕ_САМЫЕ_AAD_ДАННЫЕ"
```

#### "File not found" или "Permission denied" (Файл не найден или нет прав)
**Проблема:** Проблемы с доступом к файлу.

**Решение:**
```bash
ls -la /путь/к/файлу
cryptocore encrypt --input /полный/путь/к/файлу.txt
```

#### "MemoryError" с большими файлами
**Проблема:** Обработка очень больших файлов вызывает проблемы с памятью.

**Решение:**
```bash
split -b 100M большой_файл.bin часть_
for part in часть_*; do
    cryptocore encrypt --mode ctr --key "$KEY" \
        --input "$part" \
        --output "${part}.enc"
done
cat часть_*.enc > большой_файл.enc
```

#### "Unsupported mode" или "Unknown algorithm" (Неподдерживаемый режим или алгоритм)
**Проблема:** Использование неподдерживаемых опций.

**Решение:**
```bash
cryptocore encrypt --help
cryptocore derive --help
```

### Режим отладки

```bash
cryptocore --verbose encrypt --mode gcm --key "$KEY" --input файл.txt
cryptocore --debug derive --password "тест" --iterations 1000
cryptocore --verbose encrypt ... 2> debug.log
```

### Проблемы с производительностью

```bash
time cryptocore derive --password "тест" --iterations 10000
cryptocore derive --password "тест" --iterations 1000
openssl speed aes-256-cbc
```

## Рекомендации по безопасности

### Управление ключами

#### 1. Генерация надежных ключей
```bash
openssl rand -hex 32
cryptocore derive --password "$(openssl rand -base64 32)" \
    --iterations 100000 --length 32
```

#### 2. Безопасное хранение ключей
**Рекомендуется:**
```bash
export КЛЮЧ_ШИФРОВАНИЯ=$(openssl rand -hex 32)
cryptocore encrypt --key "$КЛЮЧ_ШИФРОВАНИЯ" ...

echo "$KEY" > /etc/cryptocore/ключ.txt
chmod 600 /etc/cryptocore/ключ.txt
chown root:root /etc/cryptocore/ключ.txt
```

**Не рекомендуется:**
```bash
cryptocore encrypt --key "мойсекретныйключ123" ...
git add ключ.txt
cryptocore encrypt --key "пароль" ...
```

#### 3. Ротация ключей
```bash
#!/bin/bash

СТАРЫЙ_КЛЮЧ="старый_ключ_hex"
НОВЫЙ_КЛЮЧ=$(openssl rand -hex 32)

for file in /data/*.enc; do
    cryptocore encrypt --decrypt --mode gcm \
        --key "$СТАРЫЙ_КЛЮЧ" \
        --input "$file" \
        --output "${file}.tmp"
    
    cryptocore encrypt --mode gcm \
        --key "$НОВЫЙ_КЛЮЧ" \
        --input "${file}.tmp" \
        --output "$file"
    
    rm "${file}.tmp"
done

echo "Ротация ключей завершена. Новый ключ: $НОВЫЙ_КЛЮЧ"
```

### Безопасность паролей

#### 1. Требования к паролям
- Минимум 12 символов
- Смесь заглавных, строчных букв, цифр, символов
- Избегайте словарных слов
- Используйте менеджеры паролей

#### 2. Безопасный ввод паролей
```bash
read -sp "Введите пароль: " ПАРОЛЬ
echo

ПАРОЛЬ=$(pass show server/encryption)
cryptocore derive --password "$ПАРОЛЬ" ...

ПАРОЛЬ=$(gpg --decrypt пароль.gpg)
cryptocore derive --password "$ПАРОЛЬ" ...
```

### Рекомендации по алгоритмам

#### Режимы шифрования
| Режим | Аутентификация | Использование | Рекомендация |
|------|---------------|----------|----------------|
| GCM | Да (AEAD) | Общее шифрование | Рекомендуется |
| CTR | Нет | Потоковое шифрование | Хорошо для потоков |
| CBC | Нет | Совместимость со старыми системами | Используйте с HMAC |
| ECB | Нет | Только для тестирования | Никогда для реальных данных |

**Всегда используйте GCM когда возможно:**
```bash
cryptocore encrypt --mode gcm --key "$KEY" --input данные.txt

cryptocore encrypt --mode ctr --key "$KEY" --input данные.txt
cryptocore hmac --key "$HMAC_KEY" --input данные.enc

cryptocore encrypt --mode ecb --key "$KEY" --input данные.txt
```

#### Хэш-функции
- Используйте SHA-256 или SHA3-256 для криптографического хэширования
- SHA-256: Стандарт NIST, широко поддерживается
- SHA3-256: Новый стандарт, другая конструкция

#### Генерация ключей
- PBKDF2 с минимум 100,000 итераций
- Используйте уникальную соль для каждого пароля
- Храните соль вместе с производным ключом
- Для продакшена: Рассмотрите Argon2 или scrypt

### Безопасность работы с файлами

#### 1. Безопасные права доступа
```bash
chmod 600 чувствительный_файл.txt
chown root:root /etc/cryptocore/
```

#### 2. Безопасное удаление
```bash
shred -u незашифрованный_файл.txt
dd if=/dev/zero of=файл.bin bs=1M count=10
rm -P файл.bin
```

#### 3. Проверка перед использованием
```bash
cryptocore hmac --key "$KEY" --input файл.enc --verify ожидаемый.hmac
if [ $? -ne 0 ]; then
    echo "Ошибка проверки целостности"
    exit 1
fi
```

### Сетевая безопасность

#### Шифрование сетевых передач
```bash
cryptocore encrypt --mode gcm --key "$KEY" \
    --input данные.tar --output данные.tar.enc

cryptocore hmac --key "$HMAC_KEY" \
    --input данные.tar.enc --output данные.tar.enc.hmac

scp данные.tar.enc данные.tar.enc.hmac user@сервер:/backup/

cryptocore hmac --key "$HMAC_KEY" \
    --input данные.tar.enc --verify данные.tar.enc.hmac
cryptocore encrypt --decrypt --mode gcm \
    --key "$KEY" --input данные.tar.enc --output данные.tar
```

## Частые вопросы

### Вопрос 1: Готов ли CryptoCore для продакшена?
**Ответ:** CryptoCore реализует стандартные криптографические алгоритмы и протестирован на тестовых векторах NIST. Однако для критически важных продакшен-систем рекомендуется использовать проверенные библиотеки типа OpenSSL или cryptography.io вместе с правильным управлением ключами и аудитом безопасности.

### Вопрос 2: Чем CryptoCore отличается от OpenSSL?
**Ответ:** CryptoCore предоставляет более простой и сфокусированный CLI интерфейс для общих операций. OpenSSL более комплексный, но имеет более сложный интерфейс. CryptoCore совместим с OpenSSL - можно шифровать одним и расшифровывать другим.

### Вопрос 3: Какой максимальный размер файла поддерживается?
**Ответ:** CryptoCore обрабатывает файлы любого размера, используя потоковую обработку. Протестировано с файлами более 10GB. Ограничение - доступное место на диске и память.

### Вопрос 4: Как восстановить данные, если забыл пароль?
**Ответ:** Нельзя. Модель безопасности предполагает, что только авторизованные пользователи с правильным паролем или ключом могут расшифровать данные. Всегда храните безопасные резервные копии ключей шифрования.

### Вопрос 5: Можно ли использовать CryptoCore в скриптах?
**Ответ:** Да, CryptoCore разработан для использования в скриптах. Используйте флаг `--quiet` для машинно-читаемого вывода и корректных кодов завершения для обработки ошибок.

### Вопрос 6: Безопасно ли шифровать образы ВМ или базы данных?
**Ответ:** Для активных баз данных используйте встроенное шифрование СУБД. Для резервных копий CryptoCore хорошо подходит. Для образов ВМ убедитесь, что у вас достаточно места для зашифрованного вывода.

### Вопрос 7: Как обновить CryptoCore?
**Ответ:** 
```bash
pip install --upgrade cryptocore
или из исходного кода:
cd CryptoCore
git pull
pip install -e .
```

### Вопрос 8: Можно ли внести вклад в разработку?
**Ответ:** Да. Смотрите CONTRIBUTING.md для инструкций. Вклады должны включать тесты и обновления документации.

### Вопрос 9: Как сообщать об уязвимостях безопасности?
**Ответ:** Сообщайте об уязвимостях через GitHub issues или email. Включайте детальные шаги для воспроизведения. Не разглашайте публично до исправления.

### Вопрос 10: Работает ли CryptoCore на Windows?
**Ответ:** Да, хотя некоторые примеры с оболочкой могут требовать адаптации для Windows PowerShell или Command Prompt. Python код кроссплатформенный.

---

**Нужна помощь?**
- GitHub Issues: https://github.com/megastormdoto/CryptoCore/issues
- Используйте `--help` для любой команды
- Включите `--verbose` или `--debug` для подробного вывода
- Изучите тесты для примеров использования