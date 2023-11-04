
class Card(object):
    def __init__(
        self,
        card_name: str,
        card_number: str,
        card_valid_thru: str,
        card_ccv: int,
        is_card_default: bool
    ) -> None:
        self.validation_messages = list()

        if type(card_name) is not str:
            self.validation_messages.append("O nome impresso no cartão não é válido.")
        if len(card_name) == 0:
            self.validation_messages.append("O nome impresso no cartão não pode ser vazio.")
        
        
        if type(card_number) is not str:
            self.validation_messages.append("O número do cartão não é válido.")
        if len(card_number) == 0:
            self.validation_messages.append("O número do cartão não pode ser vazio.")
        
        
        if type(card_valid_thru) is not str:
            self.validation_messages.append("A data de validade do cartão não é válida.")
        if len(card_valid_thru) == 0:
            self.validation_messages.append("A data de validade do cartão não pode ser vazia.")
        

        if card_ccv.isnumeric() == False:
            self.validation_messages.append("O CVV do cartão não é válido.")
            card_ccv = 0
        
        self.card_name = card_name
        self.card_number = card_number
        self.card_valid_thru = card_valid_thru
        self.card_ccv = int(card_ccv)
        self.is_card_default = True if is_card_default else False
        self.card_brand = self.get_card_brand()
    
    def get_card_brand(self):
        if self.card_number[:2] == '22':
            return 'Master Card'
        elif self.card_number[:2] == '12':
            return 'Visa'
        else:
            return 'Bandeira desconhecida' 
