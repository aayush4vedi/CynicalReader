"""Flask app configuration."""
from os import environ, path
# from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from environment variables."""

    # FLASK_APP = environ.get('FLASK_APP')
    # FLASK_ENV = environ.get('FLASK_ENV')
    # SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = 'development'
    FLASK_APP = 'index.py'
    FLASK_DEBUG = 1

    # Flask-SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Thisissupposedtobesecret!'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/users.db'

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')


    #setup mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'aayush.supp@gmail.com'
    MAIL_PASSWORD = 'SupSupSup3???'

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    # COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Stripe test keys
    STRIPE_PUBLIC_KEY = 'pk_test_51HdkIZF7Uiqhzjej6i0PT2SdIPS7uYiWYyfLBcYNFrHWgr67WknIW4VTrx0ZBkqOGmYPyoWiP0dWX3UPdJXPt09v00CKwfpj5W'
    STRIPE_SECRET_KEY = 'sk_test_51HdkIZF7UiqhzjejXAHfHx1ahnVJCA4E0TN4mmV2Y1nhooN0Huacfo08o21fphcw1qDVyPjSwCPZEhekz5jARD0O00K2Qb2uEF'

    #NOTE: export them into terminal before running app
    BASIC = 'price_1HdkNJF7UiqhzjejBaQyUM3X'
    PREMIUM = 'price_1HdkNJF7UiqhzjejPkxc3rBy'

#TODO: pick everything from env(like in commented lines)
