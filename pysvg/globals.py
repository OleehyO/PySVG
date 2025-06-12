import logging


class Globals:
    """
    Singleton class for managing global variables with predefined and dynamic attributes.

    Usage Example:
        >>> # 1. Access predefined variable (with default value)
        >>> print(Globals().repo_name)  # Output: OleehyO/TexTeller

        >>> # 2. Modify predefined variable
        >>> Globals().repo_name = "NewRepo/NewProject"
        >>> print(Globals().repo_name)  # Output: NewRepo/NewProject

        >>> # 3. Dynamically add new variable
        >>> Globals().new_var = "hello"
        >>> print(Globals().new_var)  # Output: hello

        >>> # 4. View all variables
        >>> print(Globals())  # Output: <Globals: {'repo_name': ..., 'new_var': ...}>
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.logging_level = logging.INFO
            self.__class__._initialized = True

    def __repr__(self):
        return f"<Globals: {self.__dict__}>"
