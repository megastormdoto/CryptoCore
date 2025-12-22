# CryptoCore - Cryptographic Core Operations

Инструмент командной строки для шифрования, дешифрования, вычисления хэш-сумм, HMAC, GCM аутентифицированного шифрования и деривации ключей.

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/megastormdoto/CryptoCore.git
cd CryptoCore
```

### 2. Настройка виртуального окружения
```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Обновление pip
pip install --upgrade pip
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Установка проекта в режиме разработки
```bash
pip install -e .
```

### 5. Проверка установки
```bash
# Проверка работоспособности
cd src
python -c "import crypto; print('Проект успешно импортирован')"

# Проверка CLI
python -m cryptocore --help
```

## Новые возможности (Sprint 8)

### Отчет по завершению проекта CryptoCore

#### Итоги тестирования
Проект успешно прошел все основные тесты с результатом:

- **Всего тестов:** 245
- **Пройдено:** 224 (91.4%)
- **Пропущено:** 8 (3.3%)
- **Ожидаемые сбои:** 12 (4.9%)
- **Неожиданные прохождения:** 1 (0.4%)
- **Покрытие кода:** 51%

#### Завершенные работы в спринте 8

##### 1. Комплексная документация
**Документация API (API.md):**
- Полная документация всех публичных функций, классов и модулей
- Описание назначения и функциональности каждого компонента
- Сигнатуры функций с типами параметров и возвращаемых значений
- Примеры использования и рекомендации по безопасности
- Организация по модулям: AES, режимы шифрования, хэш-функции, HMAC, KDF

**Руководство пользователя (USERGUIDE.md):**
- Полные инструкции по использованию CLI инструмента
- Инструкции по установке для различных платформ
- Примеры для всех основных сценариев использования
- Раздел устранения неполадок с типичными ошибками
- Рекомендации по безопасности и управлению ключами
- Быстрая справочная таблица команд

**Руководство разработчика (DEVELOPMENT.md):**
- Инструкции по настройке среды разработки
- Структура проекта и организация кода
- Процесс запуска тестов и добавления новых функций
- Руководство по обеспечению качества кода
- Процесс сборки и дистрибуции
- Управление тестовыми векторами

**Руководство для контрибьюторов (CONTRIBUTING.md):**
- Процесс разработки и создания веток
- Правила кодирования и стиль кода
- Требования к тестированию и безопасности
- Процесс создания Pull Request
- Добавление новых алгоритмов и тестовых векторов

##### 2. Организация тестовой инфраструктуры
Создана комплексная тестовая структура:

```
tests/
├── unit/              # 99 юнит-тестов отдельных функций
├── integration/       # 19 интеграционных тестов CLI
├── vectors/          # Тестовые векторы стандартов
├── scripts/          # Вспомогательные скрипты для тестирования
└── run_tests.py      # Унифицированный запускатор тестов
```

Тестовая система включает:
- Юнит-тесты для всех публичных функций
- Известные ответы (KAT) на основе тестовых векторов NIST/RFC
- Интеграционные тесты для CLI инструмента
- Тесты обработки ошибок и граничных условий
- Тесты производительности критических операций
- Тесты совместимости с внешними инструментами (OpenSSL)

##### 3. Поддержка всех алгоритмов из спринтов 1-7
**Проверенные реализации:**
- **AES-128 шифрование** (Sprint 1-2) - Реализация с нуля, 5 режимов работы
- **CSPRNG** (Sprint 3) - Криптографически стойкий генератор случайных чисел
- **SHA-256** (Sprint 4) - Реализация хэш-функции с нуля по NIST FIPS 180-4
- **HMAC** (Sprint 5) - Реализация с нуля по RFC 2104, поддержка SHA-256 и SHA3-256
- **GCM** (Sprint 6) - Аутентифицированное шифрование по NIST SP 800-38D
- **PBKDF2 и Key Hierarchy** (Sprint 7) - Функции деривации ключей с нуля

##### 4. Верификация корректности через тестовые векторы
Все алгоритмы проверены на соответствие стандартам через известные ответы:

- **NIST SP 800-38A**: AES ECB, CBC, CFB, OFB, CTR режимы
- **NIST SP 800-38D**: GCM аутентифицированное шифрование
- **NIST FIPS 180-4**: SHA-256 тестовые векторы
- **NIST FIPS 202**: SHA3-256 тестовые векторы
- **RFC 4231**: HMAC тестовые векторы
- **RFC 6070**: PBKDF2 тестовые векторы

##### 5. Обеспечение качества и безопасности
- Проведен аудит безопасности кода
- Проверка на отсутствие хардкоженных ключей и паролей
- Обеспечение корректного управления памятью
- Реализация constant-time операций для HMAC проверок
- Использование криптографически стойкого ГСЧ
- Документирование внешних зависимостей
- Создание файла CHANGELOG.md

## Возможности по спринтам

### Sprint 1-2: AES-128 шифрование
- Режимы ECB, CBC, CFB, OFB, CTR
- Совместимость с OpenSSL
- PKCS#7 паддинг

### Sprint 3: Криптографически стойкий ГСЧ (CSPRNG)
- Автоматическая генерация ключей
- Проверка слабых ключей
- Интеграция с NIST STS

### Sprint 4: Хэш-функции
- SHA-256 реализация с нуля
- SHA3-256 через hashlib
- Обработка файлов любого размера

### Sprint 5: HMAC
- HMAC реализация с нуля по RFC 2104
- Поддержка SHA-256 и SHA3-256
- Вычисление и проверка кодов аутентичности

### Sprint 6: GCM аутентифицированное шифрование
- Реализация GCM с нуля по NIST SP 800-38D
- Поддержка AAD (дополнительных аутентифицированных данных)
- 16-байтовые аутентификационные теги
- Умножение в поле Галуа GF(2^128)
- Катастрофический отказ при ошибке аутентификации

### Sprint 7: Key Derivation Functions
- PBKDF2-HMAC-SHA256 реализация с нуля
- Key hierarchy для детерминированной деривации ключей
- Безопасное управление паролями и солями
- Конфигурируемые параметры безопасности (итерации, длина ключа)

### Sprint 8: Полировка библиотеки и документация
- Комплексная документация API и пользовательских руководств
- Организация тестовой инфраструктуры
- Верификация корректности через тестовые векторы
- Подготовка к демонстрации
- Профессиональная структура проекта

## Использование

### Основные команды

**Key Derivation (Sprint 7):**
```bash
# Деривация ключа из пароля
python -m cryptocore derive --password <password> --salt <hex_salt> --iterations <count> --length <bytes>

# Деривация из мастер-ключа
python -m cryptocore derive --master-key <hex_master_key> --context <purpose> --length <bytes>

# Сохранение в файл
python -m cryptocore derive --password <password> --output key.bin
```

**Аутентифицированное шифрование GCM (Sprint 6):**
```bash
# Шифрование с AAD
python -m cryptocore encrypt --key <hex_key> --input plain.txt --output encrypted.bin --mode gcm --aad <hex_aad>

# Дешифрование с AAD
python -m cryptocore encrypt --decrypt --key <hex_key> --input encrypted.bin --output decrypted.txt --mode gcm --aad <hex_aad>
```

**HMAC вычисление и проверка (Sprint 5):**
```bash
# Вычисление HMAC-SHA-256
python -m cryptocore hmac --algorithm sha256 --key mysecret123 --input document.pdf

# Проверка HMAC
python -m cryptocore hmac --algorithm sha256 --key mysecret123 --input document.pdf --verify document.hmac
```

**Хэширование файлов (Sprint 4):**
```bash
python -m cryptocore dgst --algorithm sha256 --input file.txt
```

**Шифрование/дешифрование (Sprint 1-3):**
```bash
python -m cryptocore encrypt --mode cbc --input data.txt --output data.enc
```

### Поддерживаемые режимы работы

| Команда | Функциональность | Спринт | Пример использования |
|---------|------------------|--------|---------------------|
| **encrypt** | Шифрование/дешифрование AES | 1-3,6 | `python -m cryptocore encrypt --mode gcm --key <hex> --input file.txt` |
| **dgst** | Хэширование и HMAC | 4-5 | `python -m cryptocore dgst --algorithm sha256 --input file.txt` |
| **hmac** | Вычисление и проверка HMAC | 5 | `python -m cryptocore hmac --key <secret> --input data.txt` |
| **derive** | Деривация ключей | 7 | `python -m cryptocore derive --password <pass> --salt <hex>` |

### Поддерживаемые режимы шифрования

| Режим | Аутентификация | AAD | Формат вывода | Рекомендация |
|-------|----------------|-----|---------------|--------------|
| **ECB** | Нет | Нет | ciphertext | Только для тестирования |
| **CBC** | Нет | Нет | IV + ciphertext | Базовое шифрование |
| **CFB** | Нет | Нет | IV + ciphertext | Потоковое шифрование |
| **OFB** | Нет | Нет | IV + ciphertext | Потоковое шифрование |
| **CTR** | Нет | Нет | IV + ciphertext | Потоковое шифрование |
| **GCM** | Да AEAD | Да | nonce(12) + ciphertext + tag(16) | Аутентифицированное шифрование |

### Поддерживаемые хэш-алгоритмы

| Алгоритм | Реализация | Стандарт | Размер вывода |
|----------|------------|----------|---------------|
| **SHA-256** | С нуля | NIST FIPS 180-4 | 256 бит |
| **SHA3-256** | hashlib | NIST FIPS 202 | 256 бит |

## Key Derivation Functions (Sprint 7)

### Реализация PBKDF2

```python
# src/kdf/pbkdf2.py
def pbkdf2_hmac_sha256(password: Union[str, bytes], salt: Union[str, bytes], 
                       iterations: int, dklen: int) -> bytes:
    """
    PBKDF2-HMAC-SHA256 implementation from scratch according to RFC 2898.
    
    Args:
        password: Password string or bytes
        salt: Salt string or bytes (hex string if contains hex chars)
        iterations: Number of iterations (100k+ recommended)
        dklen: Desired key length in bytes
    
    Returns:
        Derived key as bytes
    """
```

### Реализация Key Hierarchy

```python
# src/kdf/hkdf.py
def derive_key(master_key: bytes, context: str, length: int = 32) -> bytes:
    """
    Derive a key from a master key using deterministic HMAC-based method.
    
    Args:
        master_key: Master key as bytes (min 16 bytes recommended)
        context: Unique identifier for key's purpose (e.g., "encryption")
        length: Desired key length in bytes
    
    Returns:
        Derived key as bytes
    """
```

### Ключевые особенности Key Derivation:

- **PBKDF2 с нуля** - полная реализация по RFC 2898
- **Key stretching** - защита от brute-force через большое количество итераций
- **Уникальные соли** - автогенерация 16-байтовых криптографически случайных солей
- **Key hierarchy** - детерминированная деривация множества ключей из одного мастер-ключа
- **Безопасное управление паролями** - чтение из файлов, env переменных, интерактивный ввод
- **Очистка памяти** - пароли удаляются из памяти сразу после использования

### Примеры применения:

#### 1. Создание ключа шифрования из пароля:
```bash
# Деривация 256-битного ключа AES
python -m cryptocore derive --password "StrongPassword123!" \
    --iterations 100000 --length 32 \
    --output aes_key.bin
```

#### 2. Key hierarchy для многоключевой системы:
```bash
# Из одного мастер-ключа получить разные ключи
python -m cryptocore derive --master-key <master_hex> --context "encryption" --length 32
python -m cryptocore derive --master-key <master_hex> --context "authentication" --length 32
python -m cryptocore derive --master-key <master_hex> --context "integrity" --length 32
```

#### 3. Безопасное хранение производных ключей:
```bash
# Генерация и сохранение ключа
python -m cryptocore derive --password-file app_password.txt \
    --iterations 500000 --length 64 \
    --output master.key --output-salt used.salt
```

### Рекомендации по безопасности:

1. **Итерации PBKDF2**: Минимум 100,000 итераций для современных систем
2. **Длина соли**: Минимум 16 байт (128 бит), уникальная для каждого пароля
3. **Мастер-ключи**: Минимум 32 байта (256 бит) для key hierarchy
4. **Контексты**: Уникальные строки для разных целей ("encryption", "auth", "signing")
5. **Хранение паролей**: Никогда не храните в коде, используйте файлы или env переменные

## GCM (Sprint 6)

### Реализация GCM

```python
# src/modes/gcm.py
class GCM:
    """GCM implementation from scratch following NIST SP 800-38D"""
    
    def __init__(self, key: bytes, nonce: bytes = None):
        self.aes = AES(key)  # AES implementation from earlier sprints
        self.nonce = nonce or os.urandom(12)
        self._precompute_table()  # GHASH precomputation
        
    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """GCM encryption with AAD support"""
        # Format: nonce(12) + ciphertext + tag(16)
        
    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """GCM decryption with authentication"""
        # Raises AuthenticationError if verification fails
```

### Ключевые особенности GCM:

- **Полная реализация с нуля** - собственный код по NIST SP 800-38D
- **Поддержка AAD** - аутентификация дополнительных данных без их шифрования
- **12-байтовые nonce** - рекомендованный размер для GCM
- **16-байтовые теги аутентификации** - 128-битная аутентификация
- **Умножение в GF(2^128)** - эффективная реализация с предвычислениями
- **Катастрофический отказ** - полное удаление выходных данных при неудачной аутентификации

### Формат файлов GCM

```
[12 байт: nonce] + [ciphertext] + [16 байт: authentication tag]
```

## Структура проекта

```
cryptocore/
├── src/
│   ├── kdf/                    # Key Derivation Functions (Sprint 7)
│   │   ├── __init__.py        # Экспорт KDF функций
│   │   ├── pbkdf2.py          # PBKDF2-HMAC-SHA256 реализация
│   │   └── hkdf.py            # Key hierarchy реализация
│   ├── aead/                  # AEAD функции (Sprint 6)
│   │   ├── __init__.py        # Экспорт AEAD классов
│   │   └── encrypt_then_mac.py # Encrypt-then-MAC реализация
│   ├── modes/                 # Режимы шифрования
│   │   ├── gcm.py             # GCM реализация (Sprint 6)
│   │   ├── ecb.py             # Режим ECB
│   │   ├── cbc.py             # Режим CBC
│   │   └── ctr.py             # Режим CTR
│   ├── mac/                   # MAC функции (Sprint 5)
│   │   ├── hmac.py            # HMAC реализация
│   │   └── cmac.py            # CMAC
│   ├── hash/                  # Хэш-функции (Sprint 4)
│   │   ├── sha256.py          # SHA-256
│   │   └── sha3_256.py        # SHA3-256
│   ├── cli_parser.py          # Парсер CLI
│   └── main.py                # Главный модуль
├── tests/                      # Комплексная тестовая система
│   ├── unit/                  # Юнит-тесты отдельных функций
│   ├── integration/           # Интеграционные тесты
│   ├── vectors/               # Тестовые векторы стандартов
│   ├── scripts/               # Вспомогательные скрипты для тестирования
│   └── run_tests.py           # Унифицированный запускатор тестов
├── docs/                      # Полная документация
│   ├── API.md                 # Документация API
│   ├── USERGUIDE.md           # Руководство пользователя
│   ├── DEVELOPMENT.md         # Руководство разработчика
│   └── CONTRIBUTING.md        # Руководство для контрибьюторов
└── README.md                  # Документация
```

## Параметры командной строки

### Команда `derive` (Sprint 7):
| Параметр | Обязательный | Описание |
|----------|--------------|----------|
| `--password`, `-p` | Если нет --master-key | Пароль для PBKDF2 |
| `--password-file`, `-P` | Если нет --master-key | Файл с паролем |
| `--password-env`, `-E` | Если нет --master-key | Переменная окружения с паролем |
| `--master-key`, `-k` | Если нет password | Мастер-ключ для key hierarchy (HEX) |
| `--context`, `-c` | Только с --master-key | Контекст для деривации (например, "encryption") |
| `--salt`, `-s` | Нет (автогенерация) | Соль в HEX формате для PBKDF2 |
| `--iterations`, `-i` | Нет (по умолчанию: 100000) | Количество итераций PBKDF2 |
| `--length`, `-l` | Нет (по умолчанию: 32) | Длина ключа в байтах |
| `--algorithm`, `-a` | Нет (по умолчанию: pbkdf2) | Алгоритм деривации (pbkdf2) |
| `--output`, `-o` | Нет | Файл для сохранения ключа (бинарный) |
| `--output-salt` | Нет | Файл для сохранения сгенерированной соли |

**Формат вывода:** `KEY_HEX SALT_HEX` (соль пустая для key hierarchy)

### Команда `encrypt` с GCM (Sprint 6):
| Параметр | Обязательный | Описание |
|----------|--------------|----------|
| `--mode gcm` | Да | GCM режим аутентифицированного шифрования |
| `--key` | Да | Ключ в HEX формате (16, 24, 32 байта) |
| `--aad` | Нет | Дополнительные аутентифицированные данные в HEX |
| `--nonce` | Нет | Nonce в HEX (12 байт). Если не указан - генерируется случайно |
| `--iv` | Нет | Алиас для --nonce (обратная совместимость) |
| `--decrypt` | Нет | Режим дешифрования |
| `--input` | Да | Входной файл |
| `--output` | Да | Выходной файл |

## Тестирование

### Запуск тестов:
```bash
# Активация виртуального окружения
source venv/bin/activate

# Переход в директорию проекта
cd src

# Тестирование Key Derivation (Sprint 7)
python -m pytest tests/unit/test_pbkdf2.py -v
python -m pytest tests/unit/test_hkdf.py -v

# Тестирование GCM (Sprint 6)
python -m pytest tests/unit/test_gcm.py -v

# Тестирование безопасности GCM
python -m pytest tests/unit/test_gcm_security.py -v

# Тестирование HMAC (Sprint 5)
python -m pytest tests/unit/test_hmac.py -v

# Тестирование SHA-256 (Sprint 4)
python -m pytest tests/unit/test_sha256.py -v

# Тестирование AES (Sprint 1-2)
python -m pytest tests/unit/test_aes.py -v

# Полный набор тестов
python -m pytest tests/ -v

# Интеграционные тесты CLI
python -m pytest tests/integration/ -v
```

### Тесты Key Derivation (Sprint 7):
- **Known-Answer Tests** - проверка на тестовых векторах
- **Детерминированность** - одинаковые входы дают одинаковый выход
- **Разделение контекстов** - разные контексты дают разные ключи
- **Уникальность солей** - проверка уникальности сгенерированных солей
- **Производительность** - измерение времени для разных количеств итераций
- **Interoperability** - сравнение с OpenSSL PBKDF2

### Пример теста Key Derivation:
```python
def test_pbkdf2_sha256_vectors():
    """Test PBKDF2-HMAC-SHA256 with correct test vectors."""
    result = pbkdf2_hmac_sha256('password', 'salt', 1, 20)
    expected = bytes.fromhex('120fb6cffcf8b32c43e7225256c4f837a86548c9')
    assert result == expected
```

## Примеры полного workflow

### Защищенная передача файлов с GCM:
```bash
# 1. Отправитель шифрует с AAD
python -m cryptocore encrypt --key 00112233445566778899aabbccddeeff \
    --input confidential.pdf --output confidential.pdf.enc \
    --mode gcm --aad "sender:alice|receiver:bob|date:2024"

# 2. Получатель дешифрует с правильным AAD
python -m cryptocore encrypt --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input confidential.pdf.enc --output decrypted.pdf \
    --mode gcm --aad "sender:alice|receiver:bob|date:2024"
```

### Создание и использование ключей через KDF:
```bash
# 1. Создать ключ из пароля
python -m cryptocore derive --password "ServerMasterPass" \
    --iterations 200000 --length 32 \
    --output server_key.bin

# 2. Использовать ключ для шифрования
python -m cryptocore encrypt --key $(xxd -p server_key.bin) \
    --input database_backup.sql --output backup.enc \
    --mode gcm --aad "db_backup_2024"
```

## Важные замечания по безопасности

### Для Key Derivation (Sprint 7):
1. **Используйте минимум 100,000 итераций PBKDF2** - защита от brute-force атак
2. **Всегда используйте уникальные соли** - предотвращение rainbow table атак
3. **Минимум 16-байтовые соли** - достаточная энтропия
4. **Разные контексты для разных целей** - предотвращение смешения ключей
5. **Никогда не храните пароли в коде** - используйте файлы или env переменные
6. **Очищайте пароли из памяти** - предотвращение дампа памяти

### Для GCM (Sprint 6):
1. **Никогда не повторяйте nonce** - повторное использование разрушает безопасность
2. **Проверяйте теги аутентификации до использования данных** - принудительный порядок верификации
3. **Используйте AAD для аутентификации метаданных** - дополнительная защита
4. **Разные ключи для разных целей** - разделение ответственности
5. **Катастрофический отказ защищает от атак** - полное удаление при неудачной аутентификации

## Отладка

Если возникают проблемы:
```bash
# Активация виртуального окружения
source venv/bin/activate

# Переход в директорию src
cd src

# Проверка Key Derivation импортов
python -c "from src.kdf.pbkdf2 import pbkdf2_hmac_sha256; print('PBKDF2 import OK')"

# Проверка CLI
python -m cryptocore derive --help

# Простой тест Key Derivation
python -c "
from src.kdf.pbkdf2 import pbkdf2_hmac_sha256
result = pbkdf2_hmac_sha256('test', 'salt', 1000, 32)
print(f'Key derived: {len(result)} bytes')
"

# Тестирование производительности
python -c "
import time
from src.kdf.pbkdf2 import pbkdf2_hmac_sha256

start = time.time()
pbkdf2_hmac_sha256('password', 'salt', 10000, 32)
elapsed = time.time() - start
print(f'10,000 iterations: {elapsed:.2f} seconds')
"
