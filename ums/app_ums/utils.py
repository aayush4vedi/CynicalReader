from flask import url_for
from flask_mail import Message
from . import mail


def send_reset_email(user):
    '''
        USED: To send password reset mails
    '''
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='aayush.supp@gmail.com',
                  recipients=['diogenes.cynicaluser@gmail.com'])
                #   recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth_bp.resetpwd', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)