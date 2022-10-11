class NmmObjectBase:

    def __init__(self, name: str):
        self.__name = name
        self.__content = None

    @property
    def name(self):
        return self.__name

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content
