import os
import sys


def generate_random_bytes(num_bytes):
    """Генерирует безопасные случайные байты"""
    try:
        return os.urandom(num_bytes)
    except Exception as e:
        raise Exception(f"CSPRNG error: Cannot generate random bytes - {str(e)}")


def generate_key():
    """Генерирует 16-байтный AES ключ"""
    return generate_random_bytes(16)


def generate_iv():
    """Генерирует 16-байтный IV"""
    return generate_random_bytes(16)


def bytes_to_hex(byte_string):
    """Конвертирует байты в HEX строку"""
    return byte_string.hex()


def is_weak_key(key):
    """Проверяет слабые ключи"""
    if len(key) != 16:
        return False

    # Все нули
    if all(byte == 0 for byte in key):
        return True
    # Все 0xFF
    if all(byte == 0xFF for byte in key):
        return True
    # Последовательные байты (0x00, 0x01, 0x02...)
    sequential_up = all(key[i] == (key[0] + i) % 256 for i in range(len(key)))
    # Последовательные байты (0xFF, 0xFE, 0xFD...)
    sequential_down = all(key[i] == (key[0] - i) % 256 for i in range(len(key)))

    return sequential_up or sequential_down