from flask import Flask, render_template, request
from models.card import Card

def create_app():
    app = Flask(__name__)
    app.debug = True

    # Here would be the cards fetched from the DB
    card_list = list()

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "GET":
            if card_list:
                return render_template("home.html", card_list=card_list)
            else:
                return render_template("empty_wallet.html")
        elif request.method == "POST":
            form_class = request.form.get('form_class')

            if form_class == 'get_card_form':
                return render_template("add_card.html", card=None)
            else:
                card = Card(
                    card_name = request.form.get('card_name'),
                    card_number = request.form.get('card_number'),
                    card_valid_thru = request.form.get('card_valid_thru'),
                    card_ccv = request.form.get('card_ccv'),
                    is_card_default = request.form.get('is_card_default')
                )

                if card.validation_messages:
                    return render_template("add_card.html", card=card)
                else:
                    card_list.append(card)
                    return render_template("home.html",card_list=card_list)
    
    return app
