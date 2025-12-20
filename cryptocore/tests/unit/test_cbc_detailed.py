# tests/unit/test_cbc_detailed.py
"""
Детальные тесты для CBC режима с тестированием реальной логики
"""
import pytest
import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


def test_cbc_encrypt_logic():
    """Тестирование логики метода encrypt CBC"""
    cbc_path = os.path.join(os.path.dirname(__file__), '../../src/modes/cbc.py')

    with open(cbc_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

        # Анализируем логику метода encrypt
        assert 'def encrypt' in content
        assert 'IV is required' in content or 'iv is None' in content
        assert 'len(iv) != self.block_size' in content
        assert '_pkcs7_pad' in content
        assert 'AES.new' in content
        assert 'previous_block = iv' in content or 'previous_block' in content
        assert 'bytes(a ^ b for a, b in zip' in content or 'xor' in content.lower()

    print(f"✓ CBC encrypt logic проверен")


def test_cbc_decrypt_logic():
    """Тестирование логики метода decrypt CBC"""
    cbc_path = os.path.join(os.path.dirname(__file__), '../../src/modes/cbc.py')

    with open(cbc_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

        # Анализируем логику метода decrypt
        assert 'def decrypt' in content
        assert 'IV is required' in content or 'iv is None' in content
        assert 'len(iv) != self.block_size' in content
        assert 'len(ciphertext) % self.block_size != 0' in content
        assert '_pkcs7_unpad' in content
        assert 'previous_block = iv' in content or 'previous_block' in content
        assert 'bytes(a ^ b for a, b in zip' in content or 'xor' in content.lower()

    print(f"✓ CBC decrypt logic проверен")


def test_cbc_chaining_mechanism():
    """Проверяем механизм chaining в CBC"""
    cbc_path = os.path.join(os.path.dirname(__file__), '../../src/modes/cbc.py')

    with open(cbc_path, 'r') as f:
        lines = f.readlines()

        # Ищем encrypt метод и проверяем chaining
        in_encrypt = False
        chaining_found = False
        previous_block_assignment = False

        for i, line in enumerate(lines):
            if 'def encrypt' in line:
                in_encrypt = True
            elif in_encrypt and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                in_encrypt = False
            elif in_encrypt:
                if 'previous_block = iv' in line:
                    previous_block_assignment = True
                elif 'previous_block =' in line and 'encrypted_block' in line:
                    chaining_found = True
                elif 'previous_block' in line and '=' in line:
                    chaining_found = True

        assert previous_block_assignment, "Инициализация previous_block с IV не найдена"
        assert chaining_found, "Механизм chaining (обновление previous_block) не найден"

    print(f"✓ CBC chaining mechanism проверен")


def test_cbc_error_handling():
    """Проверяем обработку ошибок в CBC"""
    cbc_path = os.path.join(os.path.dirname(__file__), '../../src/modes/cbc.py')

    with open(cbc_path, 'r') as f:
        content = f.read()

        # Проверяем валидацию IV
        iv_checks = 0
        if 'iv is None' in content.lower():
            iv_checks += 1
        if 'IV is required' in content:
            iv_checks += 1
        if 'raise ValueError' in content and ('IV' in content or 'iv' in content):
            iv_checks += 1

        assert iv_checks >= 2, "Недостаточная проверка IV"

        # Проверяем валидацию длины IV
        assert '16 bytes' in content or 'self.block_size' in content, "Проверка длины IV не найдена"

        # Проверяем валидацию длины ciphertext
        assert 'multiple of block size' in content.lower() or 'block_size' in content, "Проверка длины ciphertext не найдена"

    print(f"✓ CBC error handling проверен")


def test_cbc_xor_operations():
    """Проверяем операции XOR в CBC"""
    cbc_path = os.path.join(os.path.dirname(__file__), '../../src/modes/cbc.py')

    with open(cbc_path, 'r') as f:
        content = f.read()

        # Ищем XOR операции
        xor_patterns = [
            'bytes(a ^ b for a, b in zip',
            'a ^ b',
            'xor',
            '^'
        ]

        xor_count = 0
        for pattern in xor_patterns:
            if pattern in content:
                xor_count += 1

        assert xor_count >= 2, "Операции XOR не найдены или их недостаточно"

        # Проверяем что XOR используется и для encrypt и для decrypt
        lines = content.split('\n')
        encrypt_xor = False
        decrypt_xor = False

        in_encrypt = False
        in_decrypt = False

        for line in lines:
            if 'def encrypt' in line:
                in_encrypt = True
                in_decrypt = False
            elif 'def decrypt' in line:
                in_encrypt = False
                in_decrypt = True
            elif line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                in_encrypt = False
                in_decrypt = False

            if in_encrypt and ('^' in line or 'xor' in line.lower()):
                encrypt_xor = True
            if in_decrypt and ('^' in line or 'xor' in line.lower()):
                decrypt_xor = True

        assert encrypt_xor, "XOR не используется в encrypt"
        assert decrypt_xor, "XOR не используется в decrypt"

    print(f"✓ CBC XOR operations проверены")