
class Card(object):
    def __init__(
        self,
        card_name: str,
        card_number: str,
        card_valid_thru: str,
        card_ccv: int,
        is_card_default: bool
    ):
        self.card_name = card_name
        self.card_number = card_number
        self.card_valid_thru = card_valid_thru
        self.card_ccv = card_ccv
        self.is_card_default = is_card_default
        self.card_brand = self.get_card_brand()
    
    def get_card_brand(self):
        if self.card_number[:2] == '22':
            return 'Master Card'
        elif self.card_number[:2] == '12':
            return 'Visa'
        else:
            return '' 

            