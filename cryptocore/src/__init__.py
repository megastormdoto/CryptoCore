# src/__init__.py
# Это файл делает папку src пакетом Python

import os
import sys

# Добавляем текущую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))