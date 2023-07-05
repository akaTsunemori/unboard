class GlobalVars:
    def __init__(self) -> None:
        self.__discipline = ''
        self.__class = ''
        self.__professor = ''

    def set_professor(self, name: str) -> None:
        self.__clear()
        self.__professor = name

    def set_discipline(self, discipline: str) -> None:
        self.__clear()
        self.__discipline = discipline

    def set_class(self, cl: str) -> None:
        self.__class = cl

    def get_professor(self) -> str:
        return self.__professor

    def get_discipline(self) -> str:
        return self.__discipline

    def get_class(self) -> str:
        return self.__class

    def __clear(self) -> None:
        self.__discipline = ''
        self.__class = ''
        self.__professor = ''
