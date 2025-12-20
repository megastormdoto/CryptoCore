# Руководство для контрибьюторов CryptoCore

## Содержание
1. [Процесс разработки](#процесс-разработки)
2. [Настройка окружения](#настройка-окружения)
3. [Правила кодирования](#правила-кодирования)
4. [Тестирование](#тестирование)
5. [Безопасность](#безопасность)
6. [Документация](#документация)
7. [Процесс Pull Request](#процесс-pull-request)
8. [Добавление новых алгоритмов](#добавление-новых-алгоритмов)
9. [Управление тестовыми векторами](#управление-тестовыми-векторами)

---

## Процесс разработки

### 1. Создание ветки
```bash
# Создайте ветку от main
git checkout main
git pull origin main
git checkout -b feature/краткое-описание-фичи
```

**Соглашение по именованию веток:**
- `feature/` - для новых функций
- `fix/` - для исправления багов
- `docs/` - для документации
- `test/` - для добавления тестов
- `refactor/` - для рефакторинга

### 2. Структура коммитов
Сообщения коммитов должны следовать формату Conventional Commits:

```
тип(область): краткое описание

Подробное описание изменений (если необходимо)

Fixes #номер_issue
BREAKING CHANGE: Описание критических изменений (если есть)
```

**Типы коммитов:**
- `feat`: Новая функциональность
- `fix`: Исправление ошибки
- `docs`: Изменения в документации
- `test`: Добавление или изменение тестов
- `refactor`: Рефакторинг кода без изменения поведения
- `style`: Изменения форматирования, пробелы, точки с запятой
- `perf`: Изменения, улучшающие производительность
- `build`: Изменения в системе сборки
- `ci`: Изменения в CI конфигурации
- `chore`: Прочие изменения

**Пример:**
```
feat(gcm): добавление поддержки аутентифицированного шифрования

Реализован режим GCM согласно NIST SP 800-38D
Добавлена поддержка AAD (Additional Authenticated Data)
Добавлены тесты на test vectors из NIST

Fixes #45
```

---

## Настройка окружения

### 1. Установка зависимостей
```bash
# Клонирование репозитория
git clone https://github.com/megastormdoto/CryptoCore
cd CryptoCore

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate
# Активация (Linux/Mac)
source venv/bin/activate

# Установка в режиме разработки
pip install -e ".[dev]"
```

### 2. Инструменты разработки
```bash
# Установка всех инструментов качества кода
pip install black isort flake8 mypy pytest pytest-cov bandit safety

# Форматирование кода
black src/ tests/

# Сортировка импортов
isort src/ tests/

# Проверка стиля
flake8 src/ tests/

# Проверка типов
mypy src/

# Проверка безопасности
bandit -r src/
safety check
```

### 3. Pre-commit хуки
Создайте `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--config=.flake8]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        args: [--config-file=mypy.ini]
```

Установите хуки:
```bash
pip install pre-commit
pre-commit install
```

---

## Правила кодирования

### 1. Стиль кода
- Строгое следование **PEP 8**
- Максимальная длина строки: **88 символов** (Black)
- Использование двойных кавычек для строк документации
- Следование соглашениям об именовании:
  - `snake_case` для функций и переменных
  - `CamelCase` для классов
  - `UPPER_CASE` для констант

### 2. Type Hints
**Обязательно добавлять type hints для всех публичных функций:**
```python
def encrypt_data(
    key: bytes,
    plaintext: bytes,
    mode: str = "cbc",
    iv: Optional[bytes] = None
) -> tuple[bytes, bytes]:
    """
    Encrypt data using specified mode.
    
    Args:
        key: Encryption key (16, 24, or 32 bytes)
        plaintext: Data to encrypt
        mode: Encryption mode (cbc, gcm, ctr, etc.)
        iv: Initialization vector (if None, random IV generated)
    
    Returns:
        Tuple of (ciphertext, iv/nonce)
    
    Raises:
        ValueError: If key length is invalid
        TypeError: If inputs are wrong type
    """
    if len(key) not in (16, 24, 32):
        raise ValueError("Key must be 16, 24, or 32 bytes")
    # Implementation...
```

### 3. Docstrings
Использовать Google style docstrings:

```python
class AES:
    """AES block cipher implementation.
    
    Attributes:
        key_size (int): Size of key in bytes (16, 24, or 32)
        round_keys (list): Expanded round keys
    """
    
    def encrypt_block(self, plaintext: bytes) -> bytes:
        """Encrypt a single 16-byte block.
        
        Args:
            plaintext: 16-byte block to encrypt
        
        Returns:
            16-byte encrypted block
        
        Raises:
            ValueError: If plaintext is not 16 bytes
        
        Example:
            >>> aes = AES(b'0' * 16)
            >>> ciphertext = aes.encrypt_block(b'hello world!!!!!')
            >>> len(ciphertext)
            16
        """
        if len(plaintext) != 16:
            raise ValueError("Plaintext must be exactly 16 bytes")
        # Implementation...
```

### 4. Исключения
- Использовать конкретные исключения (`ValueError`, `TypeError`, `KeyError`)
- Создавать пользовательские исключения для криптографических ошибок:
```python
class CryptoError(Exception):
    """Base exception for cryptographic errors."""
    pass

class AuthenticationError(CryptoError):
    """Raised when authentication fails (GCM/HMAC)."""
    pass

class KeyDerivationError(CryptoError):
    """Raised when key derivation fails."""
    pass
```

### 5. Обработка памяти
**Чувствительные данные должны быть очищены:**
```python
import ctypes

def secure_erase(data: bytes) -> None:
    """Securely erase sensitive data from memory."""
    if data:
        # Overwrite with zeros
        ctypes.memset(id(data), 0, len(data))

def process_password(password: str) -> bytes:
    """Process password and securely clean memory."""
    try:
        password_bytes = password.encode('utf-8')
        # Process password...
        return derived_key
    finally:
        # Securely erase password from memory
        if 'password_bytes' in locals():
            secure_erase(password_bytes)
```

---

## Тестирование

### 1. Структура тестов
```
tests/
├── unit/              # Unit tests for individual functions
│   ├── test_aes.py
│   ├── test_gcm.py
│   ├── test_hmac.py
│   ├── test_pbkdf2.py
│   └── test_sha256.py
├── integration/       # End-to-end tests
│   ├── test_cli.py
│   └── test_interop.py
├── vectors/          # Test vectors from standards
│   ├── aes/
│   ├── gcm/
│   ├── sha256/
│   └── hmac/
├── performance/      # Performance benchmarks
└── run_tests.py     # Unified test runner
```

### 2. Требования к тестам
- **Покрытие кода**: >90% для всех публичных функций
- **Test vectors**: Использовать официальные векторы NIST/RFC
- **Edge cases**: Тестирование граничных условий
- **Отрицательные тесты**: Тестирование обработки ошибок

### 3. Запуск тестов
```bash
# Все тесты
python tests/run_tests.py --all

# Только unit тесты
python tests/run_tests.py --unit

# С покрытием кода
pytest --cov=src/cryptocore --cov-report=html

# Определенный модуль
pytest tests/unit/test_aes.py -v

# Тесты по имени
pytest -k "test_encrypt" -v
```

### 4. Пример теста
```python
"""Unit tests for AES implementation."""

import pytest
from src.ciphers.aes import AES
from tests.vectors.aes.loader import load_nist_vectors

class TestAES:
    """Test suite for AES cipher."""
    
    def test_key_expansion(self):
        """Test key expansion produces correct round keys."""
        key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
        aes = AES(key)
        assert len(aes.round_keys) == 11 * 16  # 11 round keys
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption followed by decryption returns original."""
        key = b'0' * 16
        plaintext = b'hello world!!!!!'
        aes = AES(key)
        
        ciphertext = aes.encrypt_block(plaintext)
        decrypted = aes.decrypt_block(ciphertext)
        
        assert decrypted == plaintext
    
    @pytest.mark.parametrize("vector", load_nist_vectors("ecb"))
    def test_nist_vectors(self, vector):
        """Test against NIST test vectors."""
        aes = AES(vector["key"])
        ciphertext = aes.encrypt_block(vector["plaintext"])
        assert ciphertext == vector["ciphertext"]
    
    def test_invalid_key_length(self):
        """Test that invalid key length raises ValueError."""
        with pytest.raises(ValueError):
            AES(b'short_key')
    
    def test_invalid_block_size(self):
        """Test that wrong block size raises ValueError."""
        aes = AES(b'0' * 16)
        with pytest.raises(ValueError):
            aes.encrypt_block(b'wrong_size')
```

---

## Безопасность

### 1. Критические правила
1. **Никогда не логировать** ключи, пароли, plaintext
2. **Очищать память** после использования чувствительных данных
3. **Constant-time сравнения** для MAC/HMAC проверок
4. **Проверять все входные данные** на корректность
5. **Никогда не повторять nonce** в GCM с одним ключом

### 2. Security Checklist
Перед каждым коммитом проверяйте:
- [ ] Нет хардкоженных ключей или паролей
- [ ] Чувствительные данные очищаются из памяти
- [ ] Используется криптографически стойкий ГСЧ
- [ ] Аутентификация проверяется перед использованием данных
- [ ] Нет использования устаревших алгоритмов (кроме тестов)
- [ ] Все пользовательские входные данные валидируются
- [ ] Обработка ошибок не раскрывает чувствительную информацию

### 3. Constant-time операции
```python
import hmac

def constant_time_compare(a: bytes, b: bytes) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    return hmac.compare_digest(a, b)

def verify_hmac(key: bytes, message: bytes, expected_mac: bytes) -> bool:
    """Verify HMAC using constant-time comparison."""
    actual_mac = hmac_sha256(key, message)
    return constant_time_compare(actual_mac, expected_mac)
```

---

## Документация

### 1. Обновление документации
При изменении кода обновите:
1. **API.md** - документация публичного API
2. **USERGUIDE.md** - руководство пользователя CLI
3. **DEVELOPMENT.md** - руководство разработчика
4. Соответствующие docstrings в коде

### 2. Примеры кода
Все примеры в документации должны быть рабочими:
```python
# ✅ Правильно - рабочий пример
from cryptocore.aes import AES
key = b'0' * 16
aes = AES(key)
ciphertext = aes.encrypt_block(b'hello world!!!!!')

# ❌ Неправильно - неполный пример
ciphertext = encrypt(data)  # Что такое encrypt? Откуда импорт?
```

### 3. Язык документации
- Основная документация: **английский**
- Комментарии в коде: **английский**
- Руководство пользователя: **русский/английский**

---

## Процесс Pull Request

### 1. Подготовка PR
Перед созданием Pull Request выполните:
```bash
# Обновить ветку main
git fetch origin
git rebase origin/main

# Запустить все проверки
python tests/run_tests.py --all
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
bandit -r src/
```

### 2. Шаблон PR
**Название PR:** `[тип] Краткое описание изменений`

**Описание PR:**
```markdown
## Что изменено
- Описание основных изменений
- Обоснование необходимости изменений

## Тип изменений
- [ ] Новая функциональность (non-breaking change)
- [ ] Исправление ошибки (non-breaking change)  
- [ ] Критическое изменение (breaking change)
- [ ] Обновление документации

## Тестирование
- [ ] Добавлены unit тесты
- [ ] Добавлены integration тесты
- [ ] Все тесты проходят
- [ ] Проверено на test vectors

## Checklist
- [ ] Код соответствует PEP 8
- [ ] Добавлены type hints
- [ ] Обновлена документация
- [ ] Нет security vulnerabilities
- [ ] Добавлены тесты для новых функций

## Связанные Issues
Fixes #номер_issue
```

### 3. Review Process
1. **Автоматические проверки:**
   - Все тесты проходят
   - Покрытие кода >90%
   - Проверка безопасности пройдена
   - Форматирование соответствует Black

2. **Ручной ревью:**
   - Проверка алгоритмической корректности
   - Проверка безопасности
   - Проверка документации
   - Проверка тестов

3. **Требования к аппруву:**
   - Минимум 1 approve от мейнтейнера
   - Все проверки CI пройдены
   - Конфликты разрешены

---

## Добавление новых алгоритмов

### 1. Процесс добавления
1. **Исследование:**
   - Изучить стандарт (NIST/RFC)
   - Найти официальные test vectors
   - Проанализировать требования безопасности

2. **Реализация:**
   - Создать модуль в соответствующей директории
   - Реализовать с нуля (если требуется)
   - Добавить type hints и docstrings

3. **Тестирование:**
   - Создать unit тесты
   - Добавить test vectors
   - Протестировать edge cases
   - Протестировать совместимость

4. **Интеграция:**
   - Добавить в CLI интерфейс
   - Обновить документацию
   - Добавить примеры использования

### 2. Требования к алгоритмам
- **Только стандартизированные алгоритмы** (NIST, RFC)
- **Избегать устаревших алгоритмов** (MD5, SHA1, DES)
- **Предпочитать аутентифицированное шифрование** (GCM)
- **Минимальные требования безопасности** (AES-128, SHA-256)

---

## Управление тестовыми векторами

### 1. Источники векторов
- **NIST SP 800-38A**: AES режимы
- **NIST SP 800-38D**: GCM
- **NIST FIPS 180-4**: SHA-256
- **NIST FIPS 202**: SHA3-256
- **RFC 4231**: HMAC
- **RFC 6070**: PBKDF2

### 2. Формат хранения
```
tests/vectors/
├── aes/
│   ├── ecb/
│   │   ├── key128.txt
│   │   ├── key192.txt
│   │   └── key256.txt
│   ├── cbc/
│   └── gcm/
├── sha256/
│   └── short_msg.txt
├── hmac/
│   └── rfc4231.txt
└── pbkdf2/
    └── rfc6070.txt
```

### 3. Загрузка векторов
Используйте скрипты в `scripts/download_vectors.py`:
```bash
python scripts/download_vectors.py --all
python scripts/download_vectors.py --algorithm aes
python scripts/download_vectors.py --algorithm sha256
```

---

## Контакты и поддержка

### Каналы связи:
- **Issues на GitHub**: Для багов и запросов функций
- **Pull Requests**: Для внесения изменений
- **Обсуждение кода**: В комментариях к PR

### Ответственные:
- **Главный мейнтейнер**: [megastormdoto](https://github.com/megastormdoto)
- **Ревью кода**: Команда мейнтейнеров проекта

### Политика безопасности:
Об уязвиностях безопасности сообщайте через GitHub Issues с меткой `security`. Не разглашайте уязвимости публично до исправления.
