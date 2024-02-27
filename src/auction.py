from datetime import datetime
from src.user import Participant

class Auction:
    def __init__(self, description, min_value, code, expiration_date):
        self._description = description
        self._min_value = min_value
        self._code = code
        self._status = 'INATIVO'
        self._expiration_date = expiration_date
        self._participants = []
        self._bids = None
        self._check_date()
        
        
    @property
    def status(self):
        return self._status      
    
    
    @property
    def code(self):
        return self._code      
    
    
    def start_auction(self):
        if self._status == 'EXPIRADO':
            raise Exception('Não pode iniciar um leilão expirado')
        self._status='ABERTO'
        self._bids = []
        
        
    def _check_date(self):
        current_date = datetime.today().date()
        expiration_date = datetime.strptime(self._expiration_date, '%d/%m/%Y').date()
        
        if current_date >= expiration_date: 
            self._status='EXPIRADO'
            self._bids=[]
        
    
    def finish_auction(self):
        if self._status == 'INATIVO':
            raise Exception('Um leilão inativo não pode ser finalizado')
        
        self._status='FINALIZADO' 
        
        winner = self._check_winner()
        if winner:
            return f'Parabéns {winner} pelo arremate do leilão'    
        
        
    def register_participant(self, _id, name):
        participant = Participant(_id, name)
        self._participants.append({
            'id': participant.id,
            'name': participant.name
        })
        
                
    def make_bid(self, value, participant):
        self._check_bid(value, participant)
        self._bids.append({
            'id': participant.id,
            'value': value
        })
        
        
    def _check_bid(self, value, participant):
        if {'id': participant.id, 'name': participant.name} in self._participants:
            if len(self._bids) == 0:
                if value < self._min_value:
                    raise Exception('O valor do lance não pode ser menor que o lance mínimo')

            else:   
                if participant.id == self._bids[-1]['id']:
                    raise Exception('Um mesmo participante não pode efetuar dois lances seguidos')  
                elif value <= self._bids[-1]['value']:
                    raise Exception('O lance não pode ser menor ou igual ao último')
                
    
    def _check_winner(self):
        if len(self._bids) > 0:
            greater = self._bids[-1]['value']
            _id = [d['id'] for d in self._bids if greater == d['value']][-1]
            winner = [d['name'] for d in self._participants if _id == d['id']][-1]
            return winner
        
            
    def auction_bids(self):
        auction_bids = []
        if len(self._bids) > 0:
            for bid in self._bids:
                _id, value = tuple(bid.values())
                name = [d['name'] for d in self._participants if _id == d['id']][-1]
                auction_bids.append({'name': name, 'value': value})
            return auction_bids
        return 'Não foram feitos lances nesse leilão ainda'
    
    
    def _check_min_max_bid(self):
        if len(self._bids) == 1:
            bid = self._bids[-1]
            name = [d['name'] for d in self._participants if bid['id'] == d['id']][-1]
            return [{'max': {'name': name, 'bid': bid['value']}, 'min': {'name': name, 'bid': bid['value']}}]
        
        elif len(self._bids) > 1:
            max_bid = self._bids[-1]
            min_bid = self._bids[0]
            name_max = [d['name'] for d in self._participants if max_bid['id'] == d['id']][-1]
            name_min = [d['name'] for d in self._participants if min_bid['id'] == d['id']][-1]
            return [{'max': {'name': name_max, 'bid': max_bid['value']}, 'min': {'name': name_min, 'bid': min_bid['value']}}]
        
        else:
            return 'Não foram feitos lances nesse leilão ainda'
    
    
    def get_min_max_bid(self):
        result = self._check_min_max_bid()
        return result