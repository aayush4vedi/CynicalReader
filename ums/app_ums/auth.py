"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import current_user, login_user
from .forms import (LoginForm, SignupForm, ForgetPasswordForm, ResetPasswordForm)
from .models import db, User
from .import login_manager
from .utils import send_reset_email


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard')) 

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                subscription_plan=form.subscription_plan.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            print("----->> user created: {}\n\t\t....................loggin in now....................\n".format(user))
            flash('Welcome aboard.Your account has been created!', 'success')
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.signupconfirm'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup.html',
        title='SignUp',
        form=form,
        # template='signup-page',
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