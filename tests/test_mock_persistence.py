from src.auction import Auction
from datetime import datetime as dt
from unittest.mock import Mock, patch
from src.auction_service import AuctionService
import pytest
import unittest

class TestMockPersistence(unittest.TestCase):  
    def test_must_register_an_auction_on_data_base(self):
        try:
            mock_persistence = Mock()
            service = AuctionService(mock_persistence)
            auction = Auction(1, "PS5", 1000, dt(2024, 4, 2))
            service.register_new_auction(auction)
            mock_persistence.insert.assert_called_once_with(auction)
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
            Auction(1, "PS5", 1000, dt(2024, 4, 2)),
            Auction(2, "Xbox Series X", 1500, dt(2024, 4, 2))
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
                       
                       
    def test_update_auction_success(self):
        # Configuração do mock
        mock_persistence = Mock()
        mock_persistence.read.return_value = [Auction(1, "PS5", 1000.0, dt(2024, 4, 22))]
        
        service = AuctionService(mock_persistence)
        service.update_auction(id=1, name="Xbox", initial_value=1000.0, closing_date=dt(2024, 4, 22))
        
        # Verifica se o método reload foi chamado
        mock_persistence.reload.assert_called_once()
    
    
    def test_update_auction_invalid_id(self):
        mock_persistence = Mock()
        service = AuctionService(mock_persistence)
        with self.assertRaises(RuntimeError):
            service.update_auction(None, name="PS5", initial_value=1000.0, closing_date=dt(2024, 4, 22))
    
    
    def test_update_auction_auction_not_found(self):
        # Configuração do mock
        mock_persistence = Mock()
        mock_persistence.read.return_value = [Auction(1, "PS5", 1000.0, dt(2024, 4, 22))]
        
        service = AuctionService(mock_persistence)
        with self.assertRaises(RuntimeError):
            service.update_auction(2, name="PS5", initial_value=1000.0, closing_date=dt(2024, 4, 22))