from enum import Enum


class Category(Enum):
    BULLY = 'bully'
    SCIENTIST = 'Scientist'
    SCHOOLBOY = 'Schoolboy'


class Language(Enum):
    ENGLISH = 'en'
    FRENCH = 'fr'
    RUSSIAN = 'ru'
    UKRAINE = 'uk'

    @classmethod
    def from_initials(cls, initials: str):
        for language in cls:
            if language.value == initials.lower():
                return language
        return None


def get_all_categories():
    return list(Category.__members__.keys())


# Функция для проверки существования категории
def check_category_exists(category_name: str) -> bool:
    return category_name in Category.__members__
