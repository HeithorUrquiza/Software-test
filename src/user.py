class User:
    def __init__(self, _id, name, password, login):
        self._id = _id
        self._name = name
        
    
    @property
    def id(self):
        return self._id
    
    
    @property
    def name(self):
        return self._name
    
    
    @property
    def name(self):
        return self._name
    
    
    @property
    def name(self):
        return self._name
    
    
if __name__ == "__main__":
    luc = User(1, 'Lucas', '123', 'luc')
    print(luc.name)