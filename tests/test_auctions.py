from src.auction import Auction
from src.user import User
from src.bid import Bid
from datetime import datetime as dt
from unittest.mock import Mock
from src.auction_service import AuctionService
import pytest
import unittest

 
class TestAuctions(unittest.TestCase):
    def setUp(self):
        self.auction = Auction(1, "PS5", 1000.0)
        self.user_1 = User(1, "Lucas", "123", "lck@gmail.com")
        self.user_2 = User(2, "Pedro", "123", "ppl@gmail.com")
    
    
    def test_must_register_bid_when_auction_receive_one(self):
        bid = Bid(self.user_1, 1001.1, dt.now())
        entrace = self.auction.propose(bid)
        expected = True
        
        assert entrace == expected
        
        
    def test_must_register_bid_when_auction_receive_more_than_one(self):
        bid_1 = Bid(self.user_1, 1001.0, dt.now())
        bid_2 = Bid(self.user_2, 1002.0, dt.now())
        
        entrace = self.auction.propose(bid_1)
        assert entrace == True
        
        entrace = self.auction.propose(bid_2)
        assert entrace == True
    
    
    def test_must_bid_register_fail_when_value_is_0(self):
        bid = Bid(self.user_1, 0, dt.now())
        entrace = self.auction.propose(bid)
        result = False
        
        assert entrace == result
        
        
    def test_must_bid_register_fail_when_user_is_duplicated(self):
        bid_1 = Bid(self.user_1, 24, dt.now())
        bid_2 = Bid(self.user_1, 1002, dt.now())
        result = self.auction.propose(bid=bid_1)
        assert result == True
        
        result = self.auction.propose(bid=bid_2)
        assert result == False
        
#-----------------------------------------------------------------------------------------------
    
    def test_must_register_bid_when_auction_receive_propose_void(self):
        try:
            bid = Bid(self.user_1, 1001, dt.now())
            self.auction.propose_void(bid)
            assert len(self.auction.bids) > 0
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}")
            
            
    def test_must_register_bid_when_auction_receive_more_than_one_bid_on_propose_void(self):
        try:
            bid_1 = Bid(self.user_1, 1001, dt.now())
            bid_2 = Bid(self.user_2, 1002, dt.now())
            self.auction.propose_void(bid_1)
            self.auction.propose_void(bid_2)
            assert len(self.auction.bids) > 1
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}")
               
       
    def test_must_fail_when_bid_register_receive_0_on_propose_void(self):
        with pytest.raises(RuntimeError) as err:
            bid = Bid(self.user_1, 0, dt.now())
            self.auction.propose_void(bid)
            
        assert err.type is RuntimeError
       
            
    def test_must_fail_when_register_bid_receive_duplicated_user_on_propose_void(self):
        with pytest.raises(RuntimeError) as err:
            bid_1 = Bid(self.user_1, 1001, dt.now())
            bid_2 = Bid(self.user_1, 1002, dt.now())
            self.auction.propose_void(bid_1)
            self.auction.propose_void(bid_2)
            
        assert err.type is RuntimeError
        
#------------------------ aprendendo sobre mocks -------------------------------------------

    def test_must_register_an_auction_on_data_base(self):
        try:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            service.register_new_auction(self.auction)
            mock_persistence.insert.assert_called_once_with(self.auction)
        except RuntimeError as err:
            pytest.fail(f"Exceção inesperada: {err}")


    def test_must_fail_when_auction_name_is_empty(self):
        with pytest.raises(RuntimeError) as err:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            auction = Auction(1, "", 1000.0, dt.now())
            service.register_new_auction(auction)
            
        assert err.type is RuntimeError
        
        
    def test_must_fail_when_auction_name_is_None(self):
        with pytest.raises(RuntimeError) as err:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            auction = Auction(1, None, 1000.0, dt.now())
            service.register_new_auction(auction)
            
        assert err.type is RuntimeError
        
        
    def test_must_fail_when_auction_initial_value_is_None(self):
        with pytest.raises(RuntimeError) as err:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            auction = Auction(1, "PS5", None, dt.now())
            service.register_new_auction(auction)
            
        assert err.type is RuntimeError
        
        
    def test_must_fail_when_auction_initial_value_is_lower_than_0(self):
        with pytest.raises(RuntimeError) as err:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            auction = Auction(1, None, -1000, dt.now())
            service.register_new_auction(auction)
            
        assert err.type is RuntimeError
    
    
    def test_must_fail_when_auction_initial_value_is_equal_to_0(self):
        with pytest.raises(RuntimeError) as err:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            auction = Auction(1, None, 0, dt.now())
            service.register_new_auction(auction)
            
        assert err.type is RuntimeError
        
        
    def test_get_auction_must_return_an_auction_if_id_exist(self):
        mock_persistence = Mock()
        
        mock_persistence.read.return_value = [
            Auction(1, "PS5", 1000, dt.now()),
            Auction(2, "Xbox Series X", 1500, dt.now())
        ]
        
        service = AuctionService(mock_persistence)
        auction = service.get_auction(1)
        assert auction.id == 1
        assert auction.name == "PS5"
        assert auction.initial_value == 1000


    def test_get_auction_must_fail_when_id_doesnt_exist(self):
        mock_persistence = Mock()
        
        mock_persistence.read.return_value = [
            Auction(1, "PS5", 1000),
            Auction(2, "Xbox Series X", 1500)
        ]
        
        service = AuctionService(mock_persistence)
        
        with pytest.raises(RuntimeError, match="O id informado é inválido ou não existe no banco de dados"):
            service.get_auction(3)
            
            
    def test_delete_auction_if_id_is_valid(self):
        try:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            service.delete_auction(1)
            mock_persistence.delete.assert_called_once_with(1)
        except RuntimeError as err:
            pytest.fail(f"Exceção inesperada: {err}")
            
            
    def test_delete_auction_must_fail_when_id_is_invalid(self):
        mock_persistence = Mock()
        service = AuctionService(mock_persistence)
        
        with pytest.raises(RuntimeError, match="O id informado é inválido"):
            service.delete_auction(None)