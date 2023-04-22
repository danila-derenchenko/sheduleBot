class Student:
    def __init__(self,name,id):
        self.__name = name
        self.__id = id
    def GetName(self):
        return self.__name
    def GetId(self):
        return self.__id