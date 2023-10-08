from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aSecretKey'  # Used for flash messaging
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'

db = SQLAlchemy(app)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Homework, Exam, Activity
    priority = db.Column(db.String(50), nullable=False)  # High, Medium, Low
    due_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500))

@app.route('/')
def index():
    assignments = Assignment.query.all()
    return render_template('index.html', assignments=assignments)

@app.route('/add', methods=['POST'])
def add_assignment():
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    description = request.form.get('description')
    category = request.form.get('category')
    priority = request.form.get('priority')

    new_assignment = Assignment(title=title, due_date=datetime.strptime(due_date, '%Y-%m-%d'), 
                                description=description, category=category, priority=priority)
    db.create_all()  # Use this to auto-update the database schema
    db.session.add(new_assignment)
    db.session.commit()

    flash("Assignment added successfully!")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_assignment(id):
    assignment = Assignment.query.get(id)
    db.session.delete(assignment)
    db.session.commit()

    flash("Assignment deleted successfully!")
    return redirect(url_for('index'))

def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
