from src.user import User
from datetime import datetime

class Bid():
    def __init__(self, user: User, value: float, dataHour: datetime):
        self._user = user
        self._value = value
        self._dataHour = dataHour
        

    @property
    def user(self):
        return self._user
    
    
    @property
    def value(self):
        return self._value
    
    
    @property
    def dataHour(self):
        return self._dataHour