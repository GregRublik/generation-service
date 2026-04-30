

class ModelAlreadyExistsException(BaseException):
    """Объект уже существует"""

class ModelNotFoundException(BaseException):
    """Объект не найден"""

class ModelMultipleResultsFoundException(BaseException):
    """При ожидании одного объекта нашлось несколько экземпляров"""

class DatabaseUnavailableException(Exception):
    status_code = 503

    def __init__(self, _original_error: Exception):
        self.error = f"Database unavailable." # print(_original_error: Exception)
        super().__init__(self.error)
