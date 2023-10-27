from flask import Flask, render_template, request
from models.card import Card

def create_app():
    app = Flask(__name__)
    app.debug = True

    home_path = 'home.html'
    card_form_path = 'card_form.html'
    empty_wallet_path = 'empty_wallet.html'

    # Here would be the cards fetched from the DB
    card_list = list()

    @app.route("/home", methods=["GET"])
    def home():
        if card_list:
            return render_template(home_path, card_list=card_list)
        else:
            return render_template(empty_wallet_path)
    
    @app.route("/card-form", methods=["GET"])
    def card_form():
        return render_template(card_form_path, card=None)
   
    @app.route("/add-card", methods=["POST"])
    def add_card():
        card = Card(
            card_name = request.form.get('card_name'),
            card_number = request.form.get('card_number'),
            card_valid_thru = request.form.get('card_valid_thru'),
            card_ccv = request.form.get('card_ccv'),
            is_card_default = request.form.get('is_card_default')
        )

        if card.validation_messages:
            return render_template(card_form_path, card=card)
        else:
            if card.is_card_default:
                for c in card_list:
                    if c.is_card_default:
                        c.is_card_default = False
                
                card_list.insert(0,card)
            else:
                card_list.append(card)

            return render_template(home_path, card_list=card_list)
    
    return app
