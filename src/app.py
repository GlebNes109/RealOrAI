from flask import render_template, redirect, url_for

from flask import Flask
from flask_wtf import CSRFProtect

from src.config import settings
from src.models.forms import LoginForm, RegisterForm
from src.repository.repository import Repository

app = Flask(__name__)
app.secret_key = settings.secret_key
CSRFProtect(app)

repository = Repository()

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == 'admin' and password == 'secret':
            return redirect(url_for('dashboard'))
        else:
            pass
    return render_template('signin.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        repository.add_user(username, password)
        # return redirect(url_for('login'))
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run(port=settings.server_port, host=settings.server_host)