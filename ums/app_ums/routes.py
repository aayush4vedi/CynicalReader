"""Logged-in page routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required, logout_user
from .forms import (MailSampleNewsletterForm, LoginForm,PrepaymentForm,UpdateAccountForm)
from .models import db, User
import csv
import json

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

''' -------------------------- Non-authentication requied paths -------------------------- '''

@main_bp.route('/', methods=['GET'])
def landing():
    return render_template(
        'landing.html',
        title='Home Page',
        template = 'landing is-preload'        #just write it! needed for css of main page
    )

#TODO:
@main_bp.route('/demo', methods=['GET', 'POST'])
def demo():
    '''
        GET: show demo page
        POST: submit form; send mail & redirect to /demo with success msg
    '''
    form = MailSampleNewsletterForm()
    mail_sent = 0                 #FIXME: send mail just once
    if form.validate_on_submit():
        email=form.email.data

        #TODO: send mail
        # if mail sent successfully-> update succ_msg, else write something else in it
        flash("You've been sent a sample newsletter in mail.Please check your inbox for {}\nIt's an old one, but we hope you like it.Subscribe to get weekly newsletters".format(email))
        return redirect(url_for('main_bp.demo'))

    return render_template(
        'demo.html',
        form=form,
        title='Demo Page',
        body='Get Demo'
    )

@main_bp.route('/pricing', methods=['GET'])
def pricing():
    #TODO: redirect to dashboard if already paid for the month: https://stripe.com/docs/api/subscriptions/object
    if current_user.is_authenticated:
        return render_template(
            'pricing_authed.html',
            title='Pricing'
        )
    else:
        return render_template(
            'pricing_guest.html',
            title='Pricing'
        )

''' -------------------------- Authentication requied paths -------------------------- '''

@main_bp.route('/prepayment', methods=['GET','POST'])
@login_required
def prepayment():
    #TODO: if user alread paid: redirect to dashboard
    form = PrepaymentForm()
    print("-------> [BEFORE_SUBMISSION] current_user: {}".format(current_user))
    if form.validate_on_submit():
        current_user.subscription_plan = form.subscription_plan.data
        db.session.commit()
        return redirect(url_for('main_bp.payment'))

    #change default plan
    form.subscription_plan.default = current_user.subscription_plan
    form.process()
    return render_template(
        'prepayment.html',
        title='Prepayment',
        form=form,
        # template='dashboard-template',      # for css class
        current_user=current_user,
        body="Select the Subscription Plan"
    )

@main_bp.route('/payment', methods=['GET'])
@login_required
def payment():
    return render_template(
        'payment.html',
        title='Payment Page',
        # template='dashboard-template',      # for css class
        current_user=current_user,
        body="This is payment page"
    )

@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.html',
        title='Dashboard',
        # template='dashboard-template',      # for css class
        current_user=current_user,
        body="Dashboard"
    )

#TODO: add method for updating tree
@main_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main_bp.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template(
        'account.html', 
        title='Account',
        body="Update Profile",
        form=form
    )


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.signin'))


# @main_bp.errorhandler(404)
# def page_not_found():
#     return render_template(
#         '404.html',
#         title='404 Page',
#         body='404 Page-I am stunned!'
#     )

#================================ Tree POC:START
# @main_bp.route("/tree")
# def treepoc():
#     ''' Trying to represent tree '''

#     with open("treeSchema.json") as f:
#         data = json.load(f)
    
#     # print(">>>>>>> from flask: \n")
#     # print(json.dumps(data, indent=4))

#     existing_user_selections = ['technews', 'tech_query', 'tech_law','database']
#     unselectable_nodes = ["root","cse","prog","career","social","business","sme","fin_eco"]

#     return render_template(
#         'tree-poc.html', 
#         title='Tree Repr',
#         body="Tree Repr POC",
#         data = data,
#         unselectable_nodes=unselectable_nodes,
#         existing_user_selections = existing_user_selections,
#         MAX_ALLOWED_NODES = 6
#     )


# @main_bp.route("/treesubmit", methods=['GET','POST'])
# def treesubmit():
#     print("user selected topics: ",request.get_json())
#     return "OKKK"

#================================ Tree POC:END

#============================== ACTUALLY USED CODE
@main_bp.route("/updatepref" , methods=['GET','POST'])
@login_required
def updatepref():
    ''' Update user preference for topic '''
    if request.method == 'POST':
        ## POST: update prefrences
        print("user selected topics: ",request.get_json())
        try:
            selected_topics_list = request.get_json()
            selected_topics_list = ','.join(selected_topics_list['selectedTopics']) #list to string
            current_user.selected_topics = selected_topics_list
            db.session.commit()
            print("===> current_user.selected_topics: ",current_user.selected_topics)
            # return redirect(url_for('main_bp.account')) #not working
            return jsonify({'message': 'preference updated successfully'})
        except Exception as e:
            return jsonify(error={'message': str(e)}), 200

    unselectable_nodes = ["root","cse","prog","career","social","business","sme","fin_eco"]
    with open("treeSchema.json") as f:
        treeSchema = json.load(f)
    existing_user_selections = list(filter(None,current_user.selected_topics.split(','))) # the string to list; list & filter used to remove empty '' values
    MAX_ALLOWED_NODES = 4
    if current_user.subscription_plan == 'PREMIUM':
        MAX_ALLOWED_NODES = 999

    return render_template(
        'nodeselection.html', 
        title='Preferences',
        body="Node Selection Here",
        data = treeSchema,
        unselectable_nodes=unselectable_nodes,
        existing_user_selections = existing_user_selections,
        MAX_ALLOWED_NODES = MAX_ALLOWED_NODES
    )
        