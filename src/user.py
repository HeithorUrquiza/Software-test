class Participant:
    def __init__(self, _id, name):
        self.__id = _id
        self.__name = name
        
    
    @property
    def id(self):
        return self.__id
    
    
    @property
    def name(self):
        return self.__name