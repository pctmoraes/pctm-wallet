from flask import Blueprint, render_template, request
from models.card import Card

pages = Blueprint(
    'wallet', 
    __name__, 
    template_folder='templates', 
    static_folder='static'
)

home_html = 'home.html'
card_form_html = 'card_form.html'
empty_wallet_html = 'empty_wallet.html'
card_list = list()

@pages.route("/")
def home():
    if card_list:
        return render_template(home_html, card_list=card_list)
    else:
        return render_template(empty_wallet_html)

@pages.route("/card-form")
def card_form():
    return render_template(card_form_html, card=None)

@pages.route("/add-card", methods=["POST"])
def add_card():
    card = Card(
        card_name = request.form.get('card_name'),
        card_number = request.form.get('card_number'),
        card_valid_thru = request.form.get('card_valid_thru'),
        card_ccv = request.form.get('card_ccv'),
        is_card_default = request.form.get('is_card_default')
    )

    if card.validation_messages:
        return render_template(card_form_html, card=card)
    else:
        if card.is_card_default:
            for c in card_list:
                if c.is_card_default:
                    c.is_card_default = False
            
            card_list.insert(0,card)
        else:
            card_list.append(card)

        return render_template(home_html, card_list=card_list)
