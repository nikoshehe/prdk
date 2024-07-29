from flask import Flask, render_template, request, redirect, url_for
import stripe
from flask_mail import Mail, Message
from database import initialize_database, get_product

app = Flask(__name__)
app.config['DEBUG'] = True

# Konfigurace pro Stripe


stripe_keys = {
    'secret_key': '',
    'publishable_key': '',  
}
stripe.api_key = stripe_keys['secret_key']

# Konfigurace pro Flask-Mail
app.config.update(
    MAIL_SERVER='',   
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='', 
    MAIL_PASSWORD=''
)
mail = Mail(app)

# Inicializace databáze
initialize_database()

# Hlavní stránka s produktem DUB
@app.route('/')
def index():
    product = get_product()
    return render_template('index.html', product=product)

# Stránka košíku (GET a POST pro zobrazení a odeslání formuláře)
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        email = request.form['email']
        product = get_product()
        return render_template('cart.html', product=product, email=email, key=stripe_keys.get('publishable_key'))
    else:
        product = get_product()
        return render_template('cart.html', product=product, key=stripe_keys.get('publishable_key'))


# Platba přes Stripe (POST metoda)
@app.route('/charge', methods=['POST'])
def charge():
    email = request.form['email']
    product = get_product()

    # Stripe Payment
    try:
        charge = stripe.Charge.create(
            amount=product[2],
            currency='usd',
            description=product[1],
            source=request.form['stripeToken'],
        )
        
        # Odeslání emailů
        send_confirmation_email(email)
        send_product_email(email)
        
        return redirect(url_for('thanks'))
    except stripe.error.StripeError:
        return 'Payment Failed'

# Potvrzovací stránka (GET metoda)
@app.route('/thanks', methods=['GET'])
def thanks():
    return 'Thank you for your purchase! Confirmation email sent.'

# Funkce pro odeslání potvrzovacího emailu
def send_confirmation_email(email):
    msg = Message('Payment Confirmation', sender='stalmi.99@seznam.cz', recipients=[email])  # změnit na danuv
    msg.body = 'Thank you for your purchase! Your payment has been received.'
    mail.send(msg)

# Funkce pro odeslání emailu s produktem
def send_product_email(email):
    msg = Message('Your Product', sender='', recipients=[email]) # změnit na danuv
    msg.body = 'Here is the link to your product: '
    mail.send(msg)

if __name__ == '__main__':
    app.run()
