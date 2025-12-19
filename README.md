```markdown
# CryptoCore - Cryptographic Core Operations

Инструмент командной строки для шифрования, дешифрования, вычисления хэш-сумм, HMAC, GCM аутентифицированного шифрования и деривации ключей.

## Новые возможности (Sprint 7)

### Key Derivation Functions
- **PBKDF2-HMAC-SHA256** - реализация с нуля по RFC 2898
- **Key Hierarchy (HKDF-like)** - детерминированная деривация ключей из мастер-ключа
- **Безопасное управление паролями** - чтение из файлов, переменных окружения, интерактивный ввод
- **Автогенерация соли** - криптографически случайные 16-байтовые соли
- **Контроль производительности** - настраиваемое количество итераций (до 1,000,000+)

### Примеры использования Key Derivation:

```bash
# Базовая деривация ключа с паролем
cryptocore derive --password "MySecurePassword123!" \
    --salt a1b2c3d4e5f601234567890123456789 \
    --iterations 100000 --length 32

# Деривация с автогенерацией соли
cryptocore derive --password "AnotherPassword" \
    --iterations 500000 --length 16

# Сохранение ключа в файл
cryptocore derive --password "app_key" \
    --salt fixedappsalt --iterations 10000 \
    --length 32 --output encryption_key.bin

# Key Hierarchy: деривация из мастер-ключа
cryptocore derive --master-key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff \
    --context "encryption" --length 32

# Безопасный ввод пароля из файла
cryptocore derive --password-file password.txt \
    --salt 1234567890abcdef --iterations 100000

# Чтение пароля из переменной окружения
export APP_PASSWORD="secret"
cryptocore derive --password-env APP_PASSWORD \
    --salt a1b2c3d4 --iterations 100000
```

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

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/megastormdoto/CryptoCore
cd CryptoCore

# Установка зависимостей
pip install -r requirements.txt
```

## Использование

### Основные команды

**Key Derivation (Sprint 7):**
```bash
# Деривация ключа из пароля
cryptocore derive --password <password> --salt <hex_salt> --iterations <count> --length <bytes>

# Деривация из мастер-ключа
cryptocore derive --master-key <hex_master_key> --context <purpose> --length <bytes>

# Сохранение в файл
cryptocore derive --password <password> --output key.bin
```

**Аутентифицированное шифрование GCM (Sprint 6):**
```bash
# Шифрование с AAD
cryptocore encrypt --key <hex_key> --input plain.txt --output encrypted.bin --mode gcm --aad <hex_aad>

# Дешифрование с AAD
cryptocore encrypt --decrypt --key <hex_key> --input encrypted.bin --output decrypted.txt --mode gcm --aad <hex_aad>
```

**HMAC вычисление и проверка (Sprint 5):**
```bash
# Вычисление HMAC-SHA-256
cryptocore hmac --algorithm sha256 --key mysecret123 --input document.pdf

# Проверка HMAC
cryptocore hmac --algorithm sha256 --key mysecret123 --input document.pdf --verify document.hmac
```

**Хэширование файлов (Sprint 4):**
```bash
cryptocore dgst --algorithm sha256 --input file.txt
```

**Шифрование/дешифрование (Sprint 1-3):**
```bash
cryptocore encrypt --mode cbc --input data.txt --output data.enc
```

### Поддерживаемые режимы работы

| Команда | Функциональность | Спринт | Пример использования |
|---------|------------------|--------|---------------------|
| **encrypt** | Шифрование/дешифрование AES | 1-3,6 | `cryptocore encrypt --mode gcm --key <hex> --input file.txt` |
| **dgst** | Хэширование и HMAC | 4-5 | `cryptocore dgst --algorithm sha256 --input file.txt` |
| **hmac** | Вычисление и проверка HMAC | 5 | `cryptocore hmac --key <secret> --input data.txt` |
| **derive** | Деривация ключей | 7 | `cryptocore derive --password <pass> --salt <hex>` |

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
cryptocore derive --password "StrongPassword123!" \
    --iterations 100000 --length 32 \
    --output aes_key.bin
```

#### 2. Key hierarchy для многоключевой системы:
```bash
# Из одного мастер-ключа получить разные ключи
cryptocore derive --master-key <master_hex> --context "encryption" --length 32
cryptocore derive --master-key <master_hex> --context "authentication" --length 32
cryptocore derive --master-key <master_hex> --context "integrity" --length 32
```

#### 3. Безопасное хранение производных ключей:
```bash
# Генерация и сохранение ключа
cryptocore derive --password-file app_password.txt \
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
├── tests/
│   ├── test_pbkdf2.py         # Тесты PBKDF2 (Sprint 7)
│   ├── test_hkdf.py           # Тесты Key Hierarchy (Sprint 7)
│   ├── test_gcm.py            # Тесты GCM (Sprint 6)
│   ├── test_gcm_security.py   # Тесты безопасности GCM
│   ├── test_hmac.py           # Тесты HMAC
│   └── test_hash.py           # Тесты хэшей
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
# Тестирование Key Derivation (Sprint 7)
python tests/test_pbkdf2.py
python tests/test_hkdf.py

# Тестирование GCM (Sprint 6)
python tests/test_gcm.py

# Тестирование безопасности GCM
python tests/test_gcm_security.py

# Тестирование HMAC (Sprint 5)
python tests/test_hmac.py

# Полный набор тестов
python -m pytest tests/
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
cryptocore encrypt --key 00112233445566778899aabbccddeeff \
    --input confidential.pdf --output confidential.pdf.enc \
    --mode gcm --aad "sender:alice|receiver:bob|date:2024"

# 2. Получатель дешифрует с правильным AAD
cryptocore encrypt --decrypt \
    --key 00112233445566778899aabbccddeeff \
    --input confidential.pdf.enc --output decrypted.pdf \
    --mode gcm --aad "sender:alice|receiver:bob|date:2024"
```

### Создание и использование ключей через KDF:
```bash
# 1. Создать ключ из пароля
cryptocore derive --password "ServerMasterPass" \
    --iterations 200000 --length 32 \
    --output server_key.bin

# 2. Использовать ключ для шифрования
cryptocore encrypt --key $(xxd -p server_key.bin) \
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

## Статус реализации

### Sprint 7: Key Derivation Functions
- **PBKDF2-HMAC-SHA256** - реализация с нуля по RFC 2898
- **Key Hierarchy** - детерминированная деривация из мастер-ключа
- **CLI команда derive** - поддержка всех параметров деривации
- **Безопасное управление паролями** - чтение из файлов, env переменных
- **Автогенерация соли** - криптографически случайные 16-байтовые соли
- **Тестирование** - полный набор тестов включая производительность

### Sprint 6: GCM аутентифицированное шифрование
- **GCM реализация** - с нуля по NIST SP 800-38D
- **Поддержка AAD** - аутентификация дополнительных данных
- **Encrypt-then-MAC** - комбинированный режим шифрования
- **Катастрофический отказ** - удаление выходных данных при ошибке аутентификации

### Sprint 5: HMAC
- **HMAC реализация** - с нуля по RFC 2104
- **Поддержка SHA-256 и SHA3-256** - два алгоритма хэширования
- **Вычисление и проверка** - полный функционал HMAC

### Sprint 4: Хэш-функции
- **SHA-256 реализация** - с нуля по NIST FIPS 180-4
- **SHA3-256** - через hashlib библиотеку
- **Обработка файлов** - поддержка файлов любого размера

### Sprint 3: CSPRNG
- **Криптографический ГСЧ** - безопасная генерация ключей
- **Проверка слабых ключей** - обнаружение и отклонение слабых ключей
- **Интеграция с NIST STS** - статистические тесты случайности

### Sprint 1-2: AES-128 шифрование
- **AES-128 реализация** - базовый блок шифрования
- **5 режимов работы** - ECB, CBC, CFB, OFB, CTR
- **PKCS#7 паддинг** - корректное дополнение данных
- **Совместимость с OpenSSL** - проверка интероперабельности

## Отладка

Если возникают проблемы:
```bash
# Проверка Key Derivation импортов
python -c "from src.kdf.pbkdf2 import pbkdf2_hmac_sha256; print('PBKDF2 import OK')"

# Проверка CLI
python main.py derive --help

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
