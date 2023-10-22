from flask import Flask, render_template, request
from models.card import Card

def create_app():
    app = Flask(__name__)
    app.debug = True

    @app.route("/", methods=["GET", "POST"])
    def home():
        card = Card('','','',0,False)

        if request.method == "POST":
            if request.form.get('card_name'):
                card_ccv = int(request.form.get('card_ccv')) \
                            if request.form.get('card_ccv') \
                            and request.form.get('card_ccv').isnumeric() else 0
                
                is_card_default = True \
                                    if request.form.get('is_card_default') else False
                
                card = Card(
                    card_name = request.form.get('card_name'),
                    card_number = request.form.get('card_number'),
                    card_valid_thru = request.form.get('card_valid_thru'),
                    card_ccv = card_ccv,
                    is_card_default = is_card_default
                )
            else:
                card.card_name = 'show_form'

        return render_template("home.html",card=card)
    
    return app
