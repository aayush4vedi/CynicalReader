"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from flask_login import current_user
from .models import User


class SignupForm(FlaskForm):
    """User Sign-up Form"""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    subscription_plan = SelectField(
        'Subscription Plan',
        default=('plan1','Plan One'),
        choices = [('plan1','Plan One'),('plan2','Plan Two')]
    )
    submit = SubmitField('SignUp')


class LoginForm(FlaskForm):
    """User Log-in Form"""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ForgetPasswordForm(FlaskForm):
    '''
        To get the email id from user to be sent reset url to.
        (Reset-pwd form 1)
    '''
    email = StringField(
        'Enter the Email You are registered with us',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email'),
            DataRequired()
        ]
    )
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    ''' 
        To enter new password by the user(redirect here from link send in pwd-reset mail)
        (Reset-pwd form 2)
    '''
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Reset Password')

class UpdateAccountForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email'),
            DataRequired()
        ]
    )
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    #NOTE: not used 
    # def validate_username(self, username):
    #     if name.data != current_user.name:
    #         user = User.query.filter_by(name=name.data).first()
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one')


class MailSampleNewsletterForm(FlaskForm):
    '''  
        This is the form submitted when a visitor(non-authorised) uesr wants
        sample newsletter sent to him on mail
    '''
    email = StringField(
        'Enter Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email')
        ]
    )
    submit = SubmitField('Mail Me A Sample Newsletter')
    submit = SubmitField('Mail Me')

class PrepaymentForm(FlaskForm):
    ''' Prepayment form- asking user Subscription plan after signup & before payment'''
    subscription_plan = SelectField(
        'Subscription Plan',
        default=('plan1','Plan One'),
        choices = [('plan1','Plan One'),('plan2','Plan Two')]
    )
    submit = SubmitField('Pay')
