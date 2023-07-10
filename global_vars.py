class GlobalVars:
    '''
    This object makes sharing specific variables between
    routes/pages considerably easier.

    There's most likely a better way to do this tho.
    '''
    def __init__(self) -> None:
        self.__discipline = ''
        self.__class = ''
        self.__class_id = 0
        self.__professor = ''
        self.__professor_id = ''
        self.__email = ''
        self.__query_results = []

    def set_professor(self, name: str) -> None:
        self.clear()
        self.__professor = name

    def set_professor_id(self, id: str) -> None:
        self.__professor_id = id

    def set_discipline(self, discipline: str) -> None:
        self.clear()
        self.__discipline = discipline

    def set_class(self, cl: str) -> None:
        self.__class = cl

    def set_class_id(self, id: int) -> None:
        self.__class_id = id

    def set_email(self, email: str) -> None:
        self.__email = email

    def set_query_results(self, query_results: list) -> None:
        if query_results:
            self.__query_results = [i for i in query_results]

    def get_professor(self) -> str:
        return self.__professor

    def get_professor_id(self) -> str:
        return self.__professor_id

    def get_discipline(self) -> str:
        return self.__discipline

    def get_class(self) -> str:
        return self.__class

    def get_class_id(self) -> str:
        return self.__class_id

    def get_email(self) -> str:
        return self.__email

    def get_query_results(self) -> list:
        return self.__query_results

    def clear(self) -> None:
        self.__discipline = ''
        self.__class = ''
        self.__class_id = 0
        self.__professor = ''
        self.__professor_id = ''
        self.__email = ''
