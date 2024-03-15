from datetime import datetime
from src.user import Participant

class Auction:
    def __init__(self, description, min_value, code, expiration_date):
        self._description = description
        self._min_value = min_value
        self._code = code
        self._status = 'INATIVO'
        self._expiration_date = expiration_date
        self._participants = {}
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
        self._participants[_id] = participant.name
        
                
    def make_bid(self, value, participant):
        self._check_bid(value, participant)
        self._bids.append({
            'id': participant.id,
            'value': value
        })
        
        
    def _check_bid(self, value, participant):
        if participant.id in self._participants:
            if len(self._bids) == 0:
                if value < self._min_value:
                    raise Exception('O valor do lance não pode ser menor que o lance mínimo')
            else:
                if value <= self._bids[-1]['value']:
                    raise Exception('O lance não pode ser menor ou igual ao último')
                if self._bids[-1]['id'] == participant.id:
                    raise Exception('Um mesmo participante não pode efetuar dois lances seguidos')
                
    
    def _check_winner(self):
        if not self._bids:
            return None
        return self._participants[self._bids[-1]['id']]
        
            
    def auction_bids(self):
        if not self._bids:
            return 'Não foram feitos lances nesse leilão ainda'
        return [{'name': self._participants[bid['id']], 'value': bid['value']} for bid in self._bids]
    
    
    def _check_min_max_bid(self):
        if not self._bids:
            return 'Não foram feitos lances nesse leilão ainda'
        
        min_bid = self._bids[0]
        max_bid = self._bids[-1]
        
        return {
            'max': {'name': self._participants[max_bid['id']], 'bid': max_bid['value']},
            'min': {'name': self._participants[min_bid['id']], 'bid': min_bid['value']},
        }
    
    
    def get_min_max_bid(self):
        result = self._check_min_max_bid()
        return result