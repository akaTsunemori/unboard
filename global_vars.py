class GlobalVars:
    def __init__(self) -> None:
        self.__discipline = ''
        self.__class = ''
        self.__professor = ''
        self.__query_results = []

    def set_professor(self, name: str) -> None:
        self.__clear()
        self.__professor = name

    def set_discipline(self, discipline: str) -> None:
        self.__clear()
        self.__discipline = discipline

    def set_class(self, cl: str) -> None:
        self.__class = cl

    def set_query_results(self, query_results: list) -> None:
        self.__query_results = query_results

    def get_professor(self) -> str:
        return self.__professor

    def get_discipline(self) -> str:
        return self.__discipline

    def get_class(self) -> str:
        return self.__class
    
    def get_query_results(self) -> list:
        return self.__query_results

    def __clear(self) -> None:
        self.__discipline = ''
        self.__class = ''
        self.__professor = ''
        self.__query_results = []
