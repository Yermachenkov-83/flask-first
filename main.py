from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask-test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    person = db.Column(db.String(80), nullable=False)
    person_info = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'comment of: {self.person}'


@app.route('/')
def index():
    comments = Comments.query.order_by(Comments.date).all()
    return render_template('index.html', data=comments)


@app.route('/<int:id>/del')
def delete(id):
    comment = Comments.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        comment = request.form['comment']
        person = request.form['person']
        person_info = request.form['person_info']

        new = Comments(comment=comment, person=person, person_info=person_info)

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('create.html')


@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    new = Comments.query.get(id)
    if request.method == 'POST':
        new.comment = request.form['comment']
        new.person = request.form['person']
        new.person_info = request.form['person_info']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:

        return render_template('edit.html', comment=new)


if __name__ == '__main__':
    app.run(debug=True)