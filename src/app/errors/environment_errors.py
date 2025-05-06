from .base_error import BaseError


class EnvironmentNotFound(BaseError):
    def __init__(self, env: str):
        super().__init__(f'The environment {env} is wrong')