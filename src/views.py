from flask import (render_template, request, redirect, flash, url_for)
from flask_login import LoginManager, login_required, login_user, logout_user
from .models import SearchResult, User
from .forms import SearchForm, LoginForm
from .import app

login_manager = LoginManager()
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search')
def search():
    search_param = request.args.get('site')
    data = SearchResult.get_result(search_param)
    return render_template('result.html', results=data, search_param=search_param)


@app.route('/add-content', methods=['GET', 'POST'])
@login_required
def add_content():
    form = SearchForm()
    # import pdb; pdb.set_trace()
    if form.validate_on_submit():
        form.save()
        return redirect('search')

    return render_template('add_content.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        flash('Logged in successfully.', "success")

        next_ = request.args.get('next')

        return redirect(next_ or url_for('home'))
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You are logged out', "info")
    return redirect(url_for('home'))
