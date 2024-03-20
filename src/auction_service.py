from src.auction_persistence import AuctionPersistence
from src.auction import Auction

class AuctionService():
    def __init__(self, persistence: AuctionPersistence) -> None:
        self._persistence = persistence
    

    def register_new_auction(self, auction: Auction):
        if auction.name == None or auction.name in ["", " "]: 
            raise RuntimeError("É necessário informar o nome do leilão")
        
        if auction.initial_value == None or auction.initial_value <= 0.0:
            raise RuntimeError("É necessário um valor maior que zero para o leilão")
        
        self._persistence.insert(auction)