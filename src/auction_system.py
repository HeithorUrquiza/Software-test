class AuctionSystem:
    def __init__(self, auctions):
        self._auctions = auctions
    
    def filter_auctions(self, status):
        if len(self._auctions) > 0:
            result = [auction.code for auction in self._auctions if auction.status == status]
            return result
        raise Exception('Não há leilões para ralização de um filtro')