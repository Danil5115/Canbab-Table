from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tasks = db.relationship('Task', backref='sprint', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='To Do')
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    in_progress_at = db.Column(db.DateTime, nullable=True)
    done_at = db.Column(db.DateTime, nullable=True)



class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    tasks = db.relationship('Task', backref='person', lazy=True)
