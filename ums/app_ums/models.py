"""Database models."""
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
	'''User account model'''

	__tablename__ = 'flasklogin-users'
	id = db.Column(
		db.Integer,
		primary_key=True
	)
	name = db.Column(
		db.String(100),
		nullable=False,
		unique=False
	)
	email = db.Column(
		db.String(40),
		unique=True,
		nullable=False
	)
	password = db.Column(
		db.String(200),
		primary_key=False,
		unique=False,
		nullable=False
	)
	created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
		default=datetime.utcnow
    )
	last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
		default=datetime.utcnow
    )
	# is_subscribed = db.Column(
	# 	db.Boolean(),
	# 	unique=False
	# )
	subscription_plan = db.Column(
		db.String(40),
		unique=False,
		nullable=True
	)
	# newsletters = db.Column(
	# 	db.String(40),???????????
	# 	unique=False,
	# 	nullable=False
	# )

	def set_password(self, password):
		"""Create hashed password."""
		self.password = generate_password_hash(password, method='sha256')

	def check_password(self, password):
		"""Check hashed password."""
		return check_password_hash(self.password, password)

	#NOTE: token expires in 3hrs
	def get_reset_token(self, expires_sec = 10800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)		

	def __repr__(self):
		return '<User:: name: {}, \temail: {}, \tsubscription_plan: {}, \tcreated_on: {}, \tlast_login: {},\t password: {} >'.format(self.name,self.email,self.subscription_plan,self.created_on,self.last_login,self.password)