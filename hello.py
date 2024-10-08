from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

def check_email(form, field):
    if "@" not in field.data:
        raise ValidationError(f"Please include an '@' in the email address. '{field.data}' is missing an '@'.")

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired(), check_email])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():

    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    