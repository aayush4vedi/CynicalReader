"""Routes for user authentication."""
import flask
from flask import redirect, render_template, flash, Blueprint, request, url_for, jsonify
from flask_login import current_user, login_user
from .forms import (LoginForm, SignupForm, ForgetPasswordForm, ResetPasswordForm)
from .models import db, User
from .import login_manager
from .utils import send_reset_email
import json
import os
import stripe

# setup stripe test keys: SECRET_KEY
STRIPE_PUBLIC_KEY = 'pk_test_51HdkIZF7Uiqhzjej6i0PT2SdIPS7uYiWYyfLBcYNFrHWgr67WknIW4VTrx0ZBkqOGmYPyoWiP0dWX3UPdJXPt09v00CKwfpj5W'
STRIPE_SECRET_KEY = 'sk_test_51HdkIZF7UiqhzjejXAHfHx1ahnVJCA4E0TN4mmV2Y1nhooN0Huacfo08o21fphcw1qDVyPjSwCPZEhekz5jARD0O00K2Qb2uEF'


stripe.api_key = STRIPE_SECRET_KEY


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# @auth_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     """
#     User sign-up page.
#     GET requests serve sign-up page.
#     POST requests validate form & user creation.
#     """
#     # Bypass if user is logged in
#     if current_user.is_authenticated:
#         return redirect(url_for('main_bp.dashboard')) 

#     form = SignupForm()
#     if form.validate_on_submit():
#         existing_user = User.query.filter_by(email=form.email.data).first()
#         if existing_user is None:
#             user = User(
#                 name=form.name.data,
#                 email=form.email.data,
#                 subscription_plan=form.subscription_plan.data
#             )
#             user.set_password(form.password.data)
#             db.session.add(user)
#             db.session.commit()  # Create new user
#             print("----->> user created: {}\n\t\t....................loggin in now....................\n".format(user))
#             flash('Welcome aboard.Your account has been created!', 'success')
#             login_user(user)  # Log in as newly created user
#             return redirect(url_for('main_bp.signupconfirm'))
#         flash('A user already exists with that email address.')
#     return render_template(
#         'signup.html',
#         title='SignUp',
#         form=form,
#         # template='signup-page',
#         body="First sign up to create account with us"
#     )

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests creates a stripe user & a user in my users.db
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard')) 
    if flask.request.method == 'POST':
        # Reads application/json and returns a response
        data = json.loads(request.data)
        try:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user is None:
                # create my own custormer(along with stripeCustomerId) & store in db here
                user = User(
                    name=data['name'],
                    email=data['email']
                )
                user.set_password(data['password'])
                db.session.add(user)
                db.session.commit()  # Create new user
                # flash('Welcome aboard.Your account has been created!', 'success')
                # Create a new customer object-Stripe
                customer = stripe.Customer.create(
                    email=data['email'],
                    address={"city":"mumbai","country":"india","line1":"unr","line2":"thane","postal_code":"421005","state":"maharashtra"},
                )
                print("stripe customer created: {}".format(customer))
                login_user(user)
                return jsonify(
                    customer=customer,
                )
            flash('A user already exists with that email address.')
        except Exception as e:
            print("xxxxxxxxxxxx ERR: ",e)
            return jsonify(error=str(e)), 403
    else:
        return render_template(
            'signup-stripe.html',
            title='SignUp',
            body="First sign up to create account with us"
        )
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))  

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            #TODO: if user.paid is false; redirect to prepayment page
            return redirect(next_page or url_for('main_bp.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        # return redirect(url_for('auth_bp.login'))
    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        # template='login-page',
        body="Log in with your User account"
    )

@auth_bp.route("/resetpwd", methods=['GET', 'POST'])
def forgetpwd():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))  
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        print("\t\t...... email sent .............")
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'forgetpwd.html', 
        title='Forget Password', 
        form=form,
        body="Forget Password Form"
    )


@auth_bp.route("/resetpwd/<token>", methods=['GET', 'POST'])
def resetpwd(token):
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))  
    user = User.verify_reset_token(token)
    print("==========>>> user: {}".format(user))
    if user is None:
        flash('That is an invalid or expired token.Please try again', 'warning')
        return redirect(url_for('auth_bp.forgetpwd'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'resetpwd.html', 
        title='Reset Password', 
        form=form,
        body="Reset Password Form"
    )



''' ------------------------ @login_manager -----------------------'''

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))











''' --------------------------------- Stripe Routes ------------------------------------ '''

# Set up webhook monitoring
@auth_bp.route('/stripe-webhook', methods=['POST'])
def webhook_received():

    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        #TODO: mark customer isSubscribed = true in db
        print(data)

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        #TODO: mark customer isSubscribed = false in db
        print(data)

    if event_type == 'invoice.finalized':
        # If you want to manually send out invoices to your customers
        # or store them locally to reference to avoid hitting Stripe rate limits.
        print(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print(data)

    if event_type == 'customer.subscription.trial_will_end':
        # Send notification to your user that the trial will end
        print(data)

    return jsonify({'status': 'success'})

# to give stripe.public_key to getConfig() method in js
@auth_bp.route('/config', methods=['GET'])
def get_config():
    return jsonify(
        publishableKey=STRIPE_PUBLIC_KEY,
    )

@auth_bp.route("/prices/<customerId>", methods=['GET'])
def prices(customerId):
    print("sent customerId = ",customerId)
    return render_template(
        'prices-stripe.html', 
        title='Show Prices', 
        customerId = customerId,
        # form=form,
        body="prices"
    )

@auth_bp.route('/create-subscription', methods=['POST'])
def createSubscription():
    data = json.loads(request.data)
    print("data: ",data)
    try:

        stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=data['customerId'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId'],
            invoice_settings={
                'default_payment_method': data['paymentMethodId'],
            },
        )

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=data['customerId'],
            items=[
                {
                    'price': os.getenv(data['priceId'])
                }
            ],
            expand=['latest_invoice.payment_intent'],
        )
        #TODO: mark customer as paid in my db
        return jsonify(subscription)
    except Exception as e:
        return jsonify(error={'message': str(e)}), 200

@auth_bp.route("/account/<subscriptionId>/<priceId>/<currentPeriodEnd>/<customerId>/<paymentMethodId>", defaults={'priceHasChanged': 'false'}, methods=['GET', 'POST'])
@auth_bp.route("/account/<subscriptionId>/<priceId>/<currentPeriodEnd>/<customerId>/<paymentMethodId>/<priceHasChanged>", methods=['GET', 'POST'])
def account(subscriptionId,priceId,currentPeriodEnd,customerId,paymentMethodId,priceHasChanged):
    print("subscriptionId: {},\tpriceId: {},\tcurrentPeriodEnd: {},\tcustomerId: {},\t,paymentMethodId: {},\t".format(subscriptionId,priceId,currentPeriodEnd,customerId,paymentMethodId))
    data = {
        'subscriptionId' : subscriptionId,
        'priceId' : priceId,
        'currentPeriodEnd' : currentPeriodEnd,
        'customerId' : customerId,
        'paymentMethodId' : paymentMethodId,
    }
    
    return render_template(
        'account-stripe.html', 
        data=data,
        # form=form,
        body="account"
    )


@auth_bp.route('/retry-invoice', methods=['POST'])
def retrySubscription():
    data = json.loads(request.data)
    try:

        stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=data['customerId'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId'],
            invoice_settings={
                'default_payment_method': data['paymentMethodId'],
            },
        )

        invoice = stripe.Invoice.retrieve(
            data['invoiceId'],
            expand=['payment_intent'],
        )
        return jsonify(invoice)
    except Exception as e:
        return jsonify(error={'message': str(e)}), 200


@auth_bp.route('/retrieve-upcoming-invoice', methods=['POST'])
def retrieveUpcomingInvoice():
    data = json.loads(request.data)
    print("retrieveUpcomingInvoice@data: {}".format(data))
    try:
        # Retrieve the subscription
        subscription = stripe.Subscription.retrieve(data['subscriptionId'])

        # Retrive the Invoice
        invoice = stripe.Invoice.upcoming(
            customer=data['customerId'],
            subscription=data['subscriptionId'],
            subscription_items=[
                {
                    'id': subscription['items']['data'][0].id,
                    'deleted': True
                },
                {
                    'price': os.getenv(data['newPriceId']),
                    'deleted': False
                }
            ],
        )
        # print("retrieveUpcomingInvoice@invoice: {}".format(invoice))
        return jsonify(invoice)
    except Exception as e:
        return jsonify(error=str(e)), 403


@auth_bp.route('/cancel-subscription', methods=['POST'])
def cancelSubscription():
    data = json.loads(request.data)
    try:
         # Cancel the subscription by deleting it
        deletedSubscription = stripe.Subscription.delete(
            data['subscriptionId'])

        #TODO: update customer in my db
        return jsonify(deletedSubscription)
    except Exception as e:
        return jsonify(error=str(e)), 403


@auth_bp.route('/update-subscription', methods=['POST'])
def updateSubscription():
    data = json.loads(request.data)
    try:
        subscription = stripe.Subscription.retrieve(data['subscriptionId'])

        updatedSubscription = stripe.Subscription.modify(
            data['subscriptionId'],
            cancel_at_period_end=False,
            items=[{
                'id': subscription['items']['data'][0].id,
                'price': os.getenv(data['newPriceId']),
            }]
        )
        #TODO: update customer in my db
        return jsonify(updatedSubscription)
    except Exception as e:
        return jsonify(error=str(e)), 403


@auth_bp.route('/retrieve-customer-payment-method', methods=['POST'])
def retrieveCustomerPaymentMethod():
    data = json.loads(request.data)
    try:
        paymentMethod = stripe.PaymentMethod.retrieve(
            data['paymentMethodId'],
        )
        return jsonify(paymentMethod)
    except Exception as e:
        return jsonify(error=str(e)), 403

