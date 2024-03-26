from src.auction import Auction
from datetime import datetime as dt
import pytest
import unittest

 
class TestAuctions(unittest.TestCase):    
    def test_must_status_auction_begin_inativo(self):
        try:
            auction = Auction(1, "PS5", 1000.0, dt(2024, 4, 22))
            assert auction.status == "Inativo"
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}")   
            
            
    def test_must_status_turn_ativo_when_start_auction(self):
        try:
            auction = Auction(1, "PS5", 1000.0, dt(2024, 4, 22))
            auction.check_date()
            auction.start_auction()
            assert auction.status == "Ativo"
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}")  
            
            
    def test_must_status_turn_finalizado_when_finish_auction_ativo(self):
        try:
            auction = Auction(1, "PS5", 1000.0, dt(2024, 4, 22))
            auction.check_date()
            auction.start_auction()
            auction.finish_auction()
            assert auction.status == "Finalizado"
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}") 
            
    
    def test_must_fail_when_try_finish_inativo_auction(self):  
        auction = Auction(1, "PS5", 1000.0, dt(2024, 4, 22))
              
        with pytest.raises(RuntimeError, match="Não é possível finalizar um leilão INATIVO ou FINALIZADO"):
            auction.finish_auction()
    
    
    def test_must_fail_when_try_finish_finalizado_auction(self):
        auction = Auction(1, "PS5", 1000.0, dt(2024, 4, 22))
        auction.check_date()
        auction.start_auction()
        auction.finish_auction()
        
        with pytest.raises(RuntimeError, match="Não é possível finalizar um leilão INATIVO ou FINALIZADO"):
            auction.finish_auction()
    
    
    def test_must_fail_when_try_start_ativo_auction(self):    
        auction = Auction(1, "PS5", 1000.0, dt(2024, 4, 22))
        auction.check_date()
        auction.start_auction()
        
        with pytest.raises(RuntimeError, match="Não é possível iniciar um leilão já ATIVO ou EXPIRADO"):
            auction.start_auction()
        
        
    def test_must_auction_status_be_expirado_when_closing_date_is_lower_or_equal_than_current_date(self):
        try:
            auction = Auction(1, "PS5", 1000.0, dt(2024, 3, 26))
            auction.check_date()
            assert auction.status == "Expirado"
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}") 
            
            
    def test_must_fail_when_try_start_expirado_auction(self):    
        auction = Auction(1, "PS5", 1000.0, dt(2024, 3, 26))
        auction.check_date()
        
        with pytest.raises(RuntimeError, match="Não é possível iniciar um leilão já ATIVO ou EXPIRADO"):
            auction.start_auction()
            
            
    def test_must_status_turn_finalizado_when_finish_auction_expirado(self):
        try:
            auction = Auction(1, "PS5", 1000.0, dt(2024, 3, 25))
            auction.check_date()
            auction.finish_auction()
            assert auction.status == "Finalizado"
        except Exception as err:
            pytest.fail(f"Exceção inesperada: {err}") 