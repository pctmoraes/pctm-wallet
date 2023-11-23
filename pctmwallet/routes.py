from flask import (
    Blueprint,
    redirect, 
    render_template,
    request,
    flash,
    session,
    url_for,
    current_app
)
from passlib.hash import pbkdf2_sha256

from pctmwallet.models.card import Card

pages = Blueprint(
    'wallet',
    __name__,
    template_folder='templates',
    static_folder='static'
)

home_html = 'home.html'
wallet_html = 'wallet.html'
signup_html = 'signup.html'
card_form_html = 'card_form.html'
empty_wallet_html = 'empty_wallet.html'


@pages.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        email = request.form.get('user_email')
        password = request.form.get('user_password')

        user = current_app.db.user.find_one({"email": email})
        if user:
            if pbkdf2_sha256.verify(password, user.get("password")):
                session['email'] = email
                return redirect(url_for('wallet.wallet'))
        
            flash('Email ou senha inválidos.')
        else:
            flash('Usuário não cadastrado')
    
    return render_template(home_html)


@pages.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('user_email')
        password = request.form.get('user_password')

        current_app.db.user.insert_one(
            {
                "email": email,
                "password": pbkdf2_sha256.hash(password)
            }
        )

        flash('Usuário criado com sucesso.')
        return redirect(url_for('wallet.home'))

    return render_template(signup_html)


@pages.route("/wallet", methods=["GET", "POST"])
def wallet():
    user_email = session.get('email')
    if current_app.db.card.count_documents({"user_email": user_email}) > 0:
        user_card_list = list(current_app.db.card.find({"user_email": user_email}))

        print(user_card_list)

        return render_template(wallet_html, card_list=user_card_list)
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
        is_card_default = request.form.get('is_card_default'),
        user_email = session.get('email')
    )

    if card.validation_messages:
        return render_template(card_form_html, card=card)
    else:
        current_app.db.card.insert_one(
            {
                "card_name": card.card_name,
                "card_number": card.card_number,
                "card_valid_thru": card.card_valid_thru,
                "card_ccv": card.card_ccv,
                "is_card_default": card.is_card_default,
                "card_brand": card.card_brand,
                "user_email": card.user_email
            }
        )

        return redirect(url_for('wallet.wallet'))

@pages.route('/logout', methods=["POST"])
def logout():
    session.clear()

    return redirect(url_for('wallet.home'))