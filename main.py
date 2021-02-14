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
        return '<Comments %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)