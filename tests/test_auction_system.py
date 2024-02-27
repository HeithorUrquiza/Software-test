from src.auction import Auction
from src.user import Participant
from src.auction_system import AuctionSystem
import pytest

class TestAuctionBehave:
    def test_if_default_status_is_INATIVO(self):
       entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
       expected = 'INATIVO'
       result = entrace.status
       
       assert result == expected
       
       
    def test_if_status_turns_ABERTO_when_auction_is_started(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = 'ABERTO'
        
        entrace.start_auction()
        
        result = entrace.status
       
        assert result == expected
        
        
    def test_return_exception_when_try_start_auction_EXPIRADO(self):
        with pytest.raises(Exception) as err:
            entrace = Auction('Leilão', 20, 'LE12', '12/12/2020')
            entrace.start_auction()
            
        assert err.type is Exception

        
        
    def test_if_status_turns_EXPIRADO_when_get_expiration_date(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2020')
        expected = 'EXPIRADO'
        
        result = entrace.status
       
        assert result == expected
        
    
    def test_if_status_turns_FINALIZADO_when_auction_is_EXPIRADO(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2020')
        expected = 'FINALIZADO'

        entrace.finish_auction()
        
        result = entrace.status
       
        assert result == expected
    
    
    def test_if_status_turns_FINALIZADO_when_auction_is_ABERTO(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = 'FINALIZADO'
        
        entrace.start_auction()
        entrace.finish_auction()
        
        result = entrace.status
       
        assert result == expected
    
    
    def test_return_exception_when_try_finish_auction_INATIVO(self):
        with pytest.raises(Exception) as err:
            entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
            entrace.finish_auction()
            
        assert err.type is Exception
        
        
    def test_exception_for_bid_lower_than_min_set(self):
        with pytest.raises(Exception) as err:
            entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
            entrace.start_auction()
            entrace.register_participant(1, 'Luan')
            entrace.make_bid(18, Participant(1, 'Luan'))
            
        assert err.type is Exception
    
        
    def test_exception_for_consecutives_bid_from_same_participant(self):
        with pytest.raises(Exception) as err:
            entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
            entrace.start_auction()
            entrace.register_participant(1, 'Luan')
            entrace.make_bid(26, Participant(1, 'Luan'))
            entrace.make_bid(27, Participant(1, 'Luan'))
            
        assert err.type is Exception
        
        
    def test_exception_for_bid_lower_or_equal_than_last_bid(self):
        with pytest.raises(Exception) as err:
            entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
            entrace.start_auction()
            entrace.register_participant(1, 'Luan')
            entrace.register_participant(2, 'Luan')
            entrace.make_bid(21, Participant(1, 'Luan'))
            entrace.make_bid(21, Participant(2, 'Luan'))
            
        assert err.type is Exception
        
        
    def test_register_of_participants(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = [{'id': 1, 'name': 'Luan'}]
        
        entrace.register_participant(1, 'Luan')
       
        assert entrace._participants == expected  
        
        
    def test_if_function_can_find_the_winner(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = 'Luan'
        
        entrace.start_auction()
        
        entrace.register_participant(1, 'Luan')
        entrace.register_participant(2, 'Pedro')
        
        entrace.make_bid(20, Participant(1, 'Luan'))
        entrace.make_bid(21, Participant(2, 'Pedro'))
        entrace.make_bid(23, Participant(1, 'Luan'))

        result = entrace._check_winner()
       
        assert result == expected
        
        
    def test_if_there_is_a_winner_when_finish_auction(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = 'Parabéns Luan pelo arremate do leilão'
        
        entrace.start_auction()
        
        entrace.register_participant(1, 'Luan')
        entrace.register_participant(2, 'Pedro')
        
        entrace.make_bid(20, Participant(1, 'Luan'))
        entrace.make_bid(21, Participant(2, 'Pedro'))
        entrace.make_bid(23, Participant(1, 'Luan'))

        result = entrace.finish_auction()
       
        assert result == expected
        
        
    def test_return_of_all_bids_of_an_auction(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = [{'name': 'Luan', 'value': 21}, {'name': 'Pedro', 'value': 22}]
        
        entrace.start_auction()
        
        entrace.register_participant(1, 'Luan')
        entrace.register_participant(2, 'Pedro')
        
        entrace.make_bid(21, Participant(1, 'Luan'))
        entrace.make_bid(22, Participant(2, 'Pedro'))

        result = entrace.auction_bids()
       
        assert result == expected
        
        
    def test_return_if_there_are_not_any_bids_in_an_auction(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = 'Não foram feitos lances nesse leilão ainda'
        
        entrace.start_auction()

        result = entrace.auction_bids()
       
        assert result == expected
        
        
    def test_min_max_bids_when_len_bids_equals_1(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = [{'max': {'name': 'Luan', 'bid': 21}, 'min': {'name': 'Luan', 'bid': 21}}]
        
        entrace.start_auction()
        entrace.register_participant(1, 'Luan')
        entrace.make_bid(21, Participant(1, 'Luan'))

        result = entrace.get_min_max_bid()
       
        assert result == expected
        
    
    def test_min_max_bids_when_len_bids_greater_than_1(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = [{'max': {'name': 'Pedro', 'bid': 50}, 'min': {'name': 'Luan', 'bid': 21}}]
        
        entrace.start_auction()
        entrace.register_participant(1, 'Luan')
        entrace.register_participant(2, 'Pedro')
        entrace.make_bid(21, Participant(1, 'Luan'))
        entrace.make_bid(50, Participant(2, 'Pedro'))

        result = entrace.get_min_max_bid()
       
        assert result == expected
        
    
    def test_min_max_bids_when_len_bids_equals_0(self):
        entrace = Auction('Leilão', 20, 'LE12', '12/12/2024')
        expected = 'Não foram feitos lances nesse leilão ainda'
        
        entrace.start_auction()

        result = entrace.get_min_max_bid()
       
        assert result == expected
    
    
    def test_filter_auctions_INATIVOS(self):
        a1 = Auction('Leilão1', 20, 'LE01', '12/12/2024')
        a2 = Auction('Leilão2', 20, 'LE02', '12/12/2024')
        a3 = Auction('Leilão3', 20, 'LE03', '12/12/2024')

        a2.start_auction()
    
        entrace = [a1, a2, a3]
        expected = ['LE01', 'LE03']

        result = AuctionSystem(entrace).filter_auctions('INATIVO')
        
        assert result == expected
    
    
    def test_filter_auctions_ABERTOS(self):
        a1 = Auction('Leilão1', 20, 'LE01', '12/12/2024')
        a2 = Auction('Leilão2', 20, 'LE02', '12/12/2024')
        a3 = Auction('Leilão3', 20, 'LE03', '12/12/2024')

        a2.start_auction()
    
        entrace = [a1, a2, a3]
        expected = ['LE02']

        result = AuctionSystem(entrace).filter_auctions('ABERTO')
        
        assert result == expected
    
    def test_filter_auctions_FECHADOS(self):
        a1 = Auction('Leilão1', 20, 'LE01', '12/12/2020')
        a2 = Auction('Leilão2', 20, 'LE02', '12/12/2024')
        a3 = Auction('Leilão3', 20, 'LE03', '12/12/2024')

        a2.start_auction()
        
        a1.finish_auction()
        a2.finish_auction()
    
        entrace = [a1, a2, a3]
        expected = ['LE01', 'LE02']

        result = AuctionSystem(entrace).filter_auctions('FINALIZADO')
        
        assert result == expected
    
    def test_filter_auctions_EXPIRADOS(self):
        a1 = Auction('Leilão1', 20, 'LE01', '12/12/2020')
        a2 = Auction('Leilão2', 20, 'LE02', '12/12/2023')
        a3 = Auction('Leilão3', 20, 'LE03', '12/12/2024')
    
        entrace = [a1, a2, a3]
        expected = ['LE01', 'LE02']

        result = AuctionSystem(entrace).filter_auctions('EXPIRADO')
        
        assert result == expected
        
        
    def test_exception_filter_auctions_when_there_are_not_any_auctions(self):
        with pytest.raises(Exception) as err:
            entrace = []
            expected = ['LE01', 'LE02']

            AuctionSystem(entrace).filter_auctions('EXPIRADO')
            
        assert err.type == Exception