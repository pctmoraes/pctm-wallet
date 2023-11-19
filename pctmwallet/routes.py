from flask import (
    Blueprint,
    redirect, 
    render_template, 
    request,
    flash,
    session,
    url_for
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
card_list = list()


users = {}

@pages.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        email = request.form.get('user_email')
        password = request.form.get('user_password')
        
        if users.get(email):
            if pbkdf2_sha256.verify(password, users.get(email)):
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

        users[email] = pbkdf2_sha256.hash(password)

        flash('Usuário criado com sucesso.')
        return redirect(url_for('wallet.home'))

    return render_template(signup_html)


@pages.route("/wallet", methods=["GET", "POST"])
def wallet():
    if card_list:
        return render_template(wallet_html, card_list=card_list)
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

        return render_template(wallet_html, card_list=card_list)

@pages.route('/logout', methods=["POST"])
def logout():
    session.clear()

    return redirect(url_for('wallet.home'))