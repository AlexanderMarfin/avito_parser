from typing import Any

# Синглтон для БД


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs) -> Any:
        if cls._instance:
            return cls._instance
        cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


# pylint: disable=R0903
class Singleton(metaclass=SingletonMeta):
    """Easy use of SingletonMeta"""
