# -*- coding: iso-8859-15 -*-

import json
import unicodedata

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm as Form

from flask_mongoengine import MongoEngine
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = MongoEngine(app)


class Books(db.Document):
        name = db.StringField()
        name_unidecode = db.StringField()
        author = db.StringField()
        description = db.StringField()
        image_uri = db.StringField()
        price = db.StringField()
        url = db.StringField()
        spider = db.StringField()
        server = db.StringField()
        project = db.StringField()
        date = db.DateTimeField()

        meta = {'indexes': [
            {'fields': ['$name', "$name_unidecode"]}]}


class SearchForm(Form):
    search = StringField("Search book\'s title", validators=[DataRequired()])
    submit = SubmitField("Find")


def str_handler(string):
    if isinstance(string, str):
        return json.dumps(string)
    elif isinstance(string, unicode):
        return '''\"{0}\"'''.format(string.encode('utf-8'))


@app.route('/', methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.search.data
        return redirect(url_for('search', keyword=keyword))
    else:
        return render_template('index.html', form=form)


@app.route('/search/<keyword>')
def search(keyword):
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.search.data
        return redirect(url_for('search', keyword=keyword))
    query = Books.objects.search_text(str_handler(keyword))
    books = [dict(json.loads(i.to_json())) for i in query.order_by('+price')]
    return render_template('results.html', form=form, books=books)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
