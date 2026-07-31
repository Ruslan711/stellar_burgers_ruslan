import secrets
from typing import TypedDict


class UserData(TypedDict, total=False):
    name: str
    email: str
    password: str
    access_token: str


def generate_email() -> str:
    """Сгенерировать email в формате задания: имя_фамилия_когорта_три_цифры@домен"""
    number = secrets.randbelow(900) + 100
    return f"ruslan_bochin_8_{number}@yandex.ru"


def generate_user() -> UserData:
    """Сгенерировать данные нового пользователя."""
    return {
        "name": "Ruslan Bochin",
        "email": generate_email(),
        "password": "123456",
    }
