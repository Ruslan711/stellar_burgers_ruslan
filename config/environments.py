from dataclasses import dataclass
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {"dev": "Dev", "stage": "Stage"}[self]


@dataclass
class UserCredentials:
    name: str
    email: str
    password: str


# Два пользователя с разными email (формат из задания)
common_users = {
    "user1": UserCredentials(
        name="Ruslan Bochin",
        email="ruslan_bochin_8_001@yandex.ru",
        password="123456"
    ),
    "user2": UserCredentials(
        name="Ivan Ivanov",
        email="ivan_ivanov_8_002@yandex.ru",
        password="123456"
    ),
    "dev_user": UserCredentials(
        name="Ruslan Bochin",
        email="ruslan_bochin_8_001@yandex.ru",
        password="123456"
    ),
    "stage_user": UserCredentials(
        name="Ivan Ivanov",
        email="ivan_ivanov_8_002@yandex.ru",
        password="123456"
    ),
}


@dataclass
class EnvironmentConfig:
    url: str
    timeout: int
    default_user: str

    def __str__(self):
        return f"- URL: {self.url}"


base_url = "https://stellarburgers.education-services.ru"
environments = {
    Environment.DEV: EnvironmentConfig(base_url, 15, "dev_user"),
    Environment.STAGE: EnvironmentConfig(base_url, 10, "stage_user"),
}


def print_environment_info(env_name, user_type=None):
    """Вывод информации о тестовом окружении."""
    try:
        env = Environment(env_name)
        config = environments[env]
        user_type = user_type or config.default_user
        user = common_users.get(user_type)

        print(f"\nEnvironment: {env}")
        print(f"{config}")

        if user:
            print(f"- User: {user.email}")
        else:
            print(f"- User type '{user_type}' not found!")
    except (ValueError, KeyError):
        print(f"Environment '{env_name}' not found!")
