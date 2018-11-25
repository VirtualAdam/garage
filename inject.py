from datetime import datetime
from app import db, create_app
from app.models import User, Post
from flask_login import current_user, login_user

def posit(message):
	app = create_app()
	app.app_context().push()
	u = User.query.get(1)
	p = Post(body=message, author=u)
	db.session.add(p)
	db.session.commit()


