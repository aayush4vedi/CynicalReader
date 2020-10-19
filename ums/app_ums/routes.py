"""Logged-in page routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from .forms import (MailSampleNewsletterForm, LoginForm,PrepaymentForm,UpdateAccountForm, TreeForm)
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
def home():
    return render_template(
        'home.html',
        title='Home Page',
        body='Welcome to CynicalNews'
    )

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
    return render_template(
        'pricing.html',
        title='Pricing Page',
        body='Pricing Page'
    )

@main_bp.route('/sample1', methods=['GET'])
def sample1():
    return render_template(
        'sample1.html',
        title='Sample One',
        body='Sample NL for Plan 1'
    )

@main_bp.route('/sample2', methods=['GET'])
def sample2():
    return render_template(
        'sample2.html',
        title='Sample Two',
        body='Sample NL for Plan 2'
    )



''' -------------------------- Authentication requied paths -------------------------- '''

@main_bp.route('/signupconfirm', methods=['GET'])
@login_required
def signupconfirm():
    return render_template(
        'signupconfirm.html',
        title='SignUp Confirmation',
        # template='dashboard-template',      # for css class
        current_user=current_user,
        body="Sign Up Successful"
    )

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
    return redirect(url_for('auth_bp.login'))


# @main_bp.errorhandler(404)
# def page_not_found():
#     return render_template(
#         '404.html',
#         title='404 Page',
#         body='404 Page-I am stunned!'
#     )


# ====================== UNUSED TREE POCs :START =======================

@main_bp.route("/treepoc", methods=['GET', 'POST'])
def treepoc():
    ''' Demo for tree '''
    form = TreeForm()
    if form.validate_on_submit():
        print("----------->>>>> form data: {}".format(form.nodes.data))
        flash('Submitted Tree', 'success')
    return render_template(
        'treepoc.html', 
        title='POC Tree',
        body="Tree Page POC",
        form=form
    )

# create a helper class for each tree node
class Node(object):
    # generate new node
    def __init__(self, cluster):
        self.cluster = cluster
        self.children = []

    # append a child node to parent (self)
    def child(self, child_cluster):
        # check if child already exists in parent
        child_found = [c for c in self.children if c.cluster == child_cluster]
        if not child_found:
            # if it is a new child, create new node for this child
            _child = Node(child_cluster)
            # append new child node to parent's children list
            self.children.append(_child)
        else:
            # if the same, save this child
            _child = child_found[0]
        # return child object for later add
        return _child

    # convert the whole object to dict
    def as_dict(self):
        res = {'cluster': self.cluster}
        res['children'] = [c.as_dict() for c in self.children]
        return res

 
@main_bp.route("/treeverti")
def treeverti():
    ''' Trying to represent tree '''

    with open("treedata.json") as f:
        data = json.load(f)
    
    # print(">>>>>>> from flask: \n")
    # print(json.dumps(data, indent=4))

    return render_template(
        'treeverti.html', 
        title='Tree Repr-Vertical',
        body="Tree Repr POC-Vertical",
        data = data
    )

# NOTE: My Favourite yet.Karna toh yehi hai boss

@main_bp.route("/treehori")
def treehori():
    ''' Trying to represent tree '''

    with open("treedata2.json") as f:
        data = json.load(f)
    
    # print(">>>>>>> from flask: \n")
    # print(json.dumps(data, indent=4))

    return render_template(
        'tree2.html', 
        title='Tree Repr-Horizontal',
        body="Tree Repr POC-Horizontal",
        data = data
    )

# ====================== UNUSED TREE POCs :END =======================

@main_bp.route("/tree")
def tree():

    with open("treedata2.json") as f:
        data = json.load(f)
    
    # print(">>>>>>> from flask: \n")
    # print(json.dumps(data, indent=4))

    return render_template(
        'tree.html', 
        title='Tree Repr-Horizontal',
        body="Tree Repr POC-Horizontal",
        data = data
    )



