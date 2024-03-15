from src.user import User
from datetime import datetime as dt
from src.bid import Bid

class Auction():
    def __init__(self, _id: int, name: str, initial_value: float, user: User = None, open_data: dt = dt.now, bids: list = []) -> None:
        self._id = _id
        self._name = name
        self._initial_value = initial_value
        self._user = user
        self._open_data = open_data
        self._bids = bids
        
    
    @property
    def bids(self):
        return self._bids
    
    
    @property
    def id(self):
        return self._id
    
    
    @property
    def name(self):
        return self._name
    
    
    @property
    def initial_value(self):
        return self._initial_value
    
        
    def is_valid(self, bid: Bid):
        return bid.value > 0
    
    
    def its_whithout_bids(self):
        return len(self._bids) == 0
        
   
    def add_bid(self, bid: Bid):
        self._bids.append(bid) 
   
   
    def is_valid_bid(self, bid: Bid):
        return self.value_is_bigger(bid, self.last_bid_proposed()) and \
                self.last_user_is_not_the_same(bid)
    
    
    def last_bid_proposed(self):
        return self._bids[-1]
    
    
    def there_is_bids(self):
        return not len(self._bids) == 0
    
    
    def value_is_bigger(self, bid: Bid, last_bid: Bid):
        return bid.value > last_bid.value
        
        
    def total_user_bids_is_lower_than_5(self, user: User):
        total_bids = self.total_bids_of(user)
        return total_bids < 5
        
        
    def total_bids_of(self, user: User):
        total = 0
        for bid in self._bids:
            if bid.user == user:
                total += 1
        return total
    
        
    def propose(self, bid: Bid):
        if not self.is_valid(bid): return False
        
        if self.its_whithout_bids() or self.is_valid_bid(bid):
            self.add_bid(bid)
            return True
        return False
    
    
    def propose_void(self, bid: Bid):
        if not self.is_valid: raise RuntimeError("Lance deve ser maior que zero")

        if self.is_whithout_bids() or self.is_valid_bid(bid):
            self.add_bid(bid)
        else:
            raise RuntimeError("Erro inesperado")
        

    def last_user_is_not_the_same(self, bid: Bid):
        last_user_bid: User = self.last_bid_proposed().user
        return not last_user_bid == bid.user