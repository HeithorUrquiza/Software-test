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
        
        
    def get_auction(self, id: int):
        auctions = self._persistence.read()
        for item in auctions:
            if item.id == id:
                return item
        raise RuntimeError("O id informado é inválido ou não existe no banco de dados")
    
    
    def delete_auction(self, id: int):
        if id == None or id < 0:
            raise RuntimeError("O id informado é inválido")
        
        self._persistence.delete(id)
        
        
    def update_auction(self, id: int, **kwargs):
        auctions = self._persistence.read()
        
        if id == None or id < 0:
            raise RuntimeError("O id informado é inválido")
        
        for item in auctions:
            if item.id == id:
                item.name = kwargs["name"]
                item.initial_value = kwargs["initial_value"]
                item.closing_date = kwargs["closing_date"]
                
                self._persistence.reload(item)
                return item
                
        raise RuntimeError("O id informado não existe no banco de dados")
        
        