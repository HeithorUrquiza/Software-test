from src.auction import Auction
from src.user import User
from src.bid import Bid
from datetime import datetime as dt
import unittest
 
class TestAuctions():
    def test_bid_register_when_auction_receive_one(self):
        user = User(1, "Calvo", "12345", "calvisse@implante.com")
        auction = Auction(1, "PS5", 1000.0, user, dt.now(), [])
        bid = Bid(user, 1001.1, dt.now())
        entrace = auction.propose(bid)
        expected = True
        
        assert entrace == expected
        
        
    def test_bid_register_when_auction_receive_more_than_one(self):
        auction = Auction(1, "PS5", 1000.0, dt.now())
        calvo = User(1, "Calvo", "123", "calvo@gmail.com")
        meioHomem = User(2, "Meio Homem", "123", "meio@gmail.com")
        bid_1 = Bid(calvo, 1001.0, dt.now())
        bid_2 = Bid(meioHomem, 1002.0, dt.now())
        
        entrace = auction.propose(bid_1)
        expected = True
        
        assert entrace == expected
        
        entrace = auction.propose(bid_2)
        
        assert entrace == expected
    
    
    def test_bid_register_fail_when_value_is_0(self):
        user = User(1, "Calvo", "12345", "calvisse@implante.com")
        auction = Auction(1, "PS5", 1000.0, user, dt.now(), [])
        bid = Bid(user, 0, dt.now())
        entrace = auction.propose(bid)
        result = False
        
        assert entrace == result
    
    
    def test_bid_register_fail_when_user_is_duplicated(self):
        auction = Auction(1, "PS5", 1000.0, dt.now())
        calvo = User(1, "Calvo", "123", "calvo@gmail.com")
        bid_1 = Bid(calvo, 1001.0, dt.now())
        bid_2 = Bid(calvo, 1002.0, dt.now())
        
        entrace = auction.propose(bid_1)
        
        assert entrace == True
        
        entrace = auction.propose(bid_2)
        
        assert entrace == True