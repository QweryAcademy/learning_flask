from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired
from .models import SearchResult, User


class SearchForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    url = StringField("Url", validators=[DataRequired()])
    content = TextAreaField("Search Content", validators=[DataRequired()])

    def save(self):
        new_search = SearchResult(
            title=self.data['title'],
            url=self.data['url'], content=self.data['content'])
        new_search.save()


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField(
        "Password", widget=PasswordInput(), validators=[DataRequired()])

    def validate(self):
        result = super().validate()
        password = self.data['password']
        user = self.get_user()
        if user and password == 'password':
            return True
        self.email.errors.append("The email/password combination is wrong")
        return False

    def get_user(self):
        return User.query.filter(User.email == self.data['email']).first()
