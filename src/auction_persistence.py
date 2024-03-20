from src.auction import Auction

class AuctionPersistence():
    def __init__(self):
        self._auctions_table = []
        
        
    def insert(self, auction: Auction):
        self._auctions_table.append(auction)


    def reload(self, auction: Auction):
        for item in self._auctions_table:
            if item.id == auction.id:
                idx = self._auctions_table.index(item)
                self._auctions_table[idx] = auction 


    def delete(self, id: int):
        for item in self._auctions_table:
            if item.id == id:
                self._auctions_table.remove(item)
        

    def read(self):
        return self._auctions_table