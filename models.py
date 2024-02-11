from WebApp import db  

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, default=0) 
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)