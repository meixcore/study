import hashlib
import os
import base64
import hmac

class HashPasswordClient:
    iteration_count = 100_000
    salt_length = 16

    def hash_password(self, raw_password: str) -> str:
        # принимает на вход строку с сырым паролем, вычисляет хеш и
        # возвращает хеш-сумму в виде строки
        salt = os.urandom(self.salt_length)

        password_bytes = raw_password.encode("utf-8")
        hash_bytes = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password_bytes,
            salt=salt,
            iterations=self.iteration_count,
        )

        salt_b64 = base64.b64encode(salt).decode("utf-8")
        hash_b64 = base64.b64encode(hash_bytes).decode("utf-8")

        return f"{salt_b64}${hash_b64}"

    def validate_password(self, input_password: str, hashed_password: str) -> bool:
        # принимает на вход 2 строки с введенным паролем и хеш-суммой пароля,
        # сравнивает их и возвращает тру если сумма от input_password
        # соответствует hashed_password
        salt_b64, hash_b64 = hashed_password.split("$")
        salt = base64.b64decode(salt_b64)
        original_hash = base64.b64decode(hash_b64)

        password_bytes = input_password.encode("utf-8")
        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password_bytes,
            salt,
            self.iteration_count,
        )

        return hmac.compare_digest(new_hash, original_hash)

client = HashPasswordClient()
password = "qwerty123"

hash1 = client.hash_password(password)
hash2 = client.hash_password(password)

print(hash1)
print(hash2)
print(client.validate_password(password, hash1))
print(client.validate_password(password, hash2))