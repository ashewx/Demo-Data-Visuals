from app import db

class User(db.Model):
	userid = db.Column(db.Integer, index=True, primary_key=True, nullable=False)
	name = db.Column(db.String, index=True, nullable=False)

class Movie(db.Model):
	movieid = db.Column(db.Integer, index=True, primary_key=True, nullable=False)
	title = db.Column(db.String, index=True, nullable=False)
		
class TagInfo(db.Model):
	tagid = db.Column(db.Integer, index=True, primary_key=True, nullable=False)
	content = db.Column(db.String, index=True, nullable=False)
		
class Genre(db.Model):
	genreid = db.Column(db.Integer, index=True, primary_key=True, nullable=False)
	name = db.Column(db.String, index=True, nullable=False)