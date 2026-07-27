import random
import time


def generate_email():
    """Сгенерировать email в формате задания."""
    number = random.randint(100, 999)
    timestamp = int(time.time()) % 10000
    return f"ruslan_bochin_8_{number}{timestamp}@yandex.ru"


def generate_user():
    """Сгенерировать данные нового пользователя."""
    return {
        "name": "Ruslan Bochin",
        "email": generate_email(),
        "password": "123456",
    }
