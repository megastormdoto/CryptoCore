#!/usr/bin/env python3
import sys
import os
import hashlib

sys.path.insert(0, 'src')

from hash.sha3_256 import SHA3_256

print("🧪 Тест SHA3-256")
print("=" * 60)

test_cases = [
    (b"", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
    (b"abc", "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
    (b"hello world", "644bcc7e564373040999aac89e7622f3ca71fba1d972fd94a31c3bfbf24e3938"),
]

all_pass = True
for data, expected in test_cases:
    hasher = SHA3_256()
    result = hasher.hash(data)

    lib_hash = hashlib.sha3_256(data).hexdigest()

    match = (result == expected) and (result == lib_hash)
    all_pass = all_pass and match

    status = "✅" if match else "❌"
    desc = f"{len(data)} байт" if data else "пустая строка"
    print(f"{status} {desc}")

    if not match:
        print(f"  Наша:      {result}")
        print(f"  Ожидалось: {expected}")
        print(f"  hashlib:   {lib_hash}")

print("\n" + "=" * 60)
if all_pass:
    print("🎉 SHA3-256 работает корректно!")
else:
    print("💥 SHA3-256 имеет проблемы")