from config import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String, nullable = True)
    
    subjects = db.relationship("Subject", backref='user',lazy=True)

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True) 
    section = db.Column(db.String(50), nullable=False)
    subject_id = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.Float, nullable=False)
    grade = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# class BackSubject(db.Model):
#     __tablename__ = 'back_subjects'

#     category = db.Column(db.String(80), nullable=False)
#     unit = db.Column(db.Float, nullable=False)
#     grade = db.Column(db.Float, nullable=False)


#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
