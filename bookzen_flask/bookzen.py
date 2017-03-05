# -*- coding: iso-8859-15 -*-
import json
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

from flask import Flask, render_template, redirect, url_for

from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

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

    def __repr__(self):
        return "{0} - {1} - {2}".format(self.name, self.spider, self.price)


class SearchForm(Form):
    flash_msg = "Please search something so we can serve you"
    search = StringField("Search book\'s title", validators=[DataRequired(flash_msg)])
    submit = SubmitField()


class ContactForm(Form):
    flash_msg = "Oops, look like you forget to fill this field."
    name = StringField("Name", [DataRequired(flash_msg)])
    email = StringField("Email", [Email(flash_msg)])
    subject = StringField("Subject", [DataRequired(flash_msg)])
    message = TextAreaField("Message", [DataRequired(flash_msg)])
    submit = SubmitField()


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
    if books:
        return render_template('results.html', form=form, books=books)
    else:
        return render_template('not_found.html', form=form)


@app.route('/contact/', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = MIMEMultipart()
        fromaddr = form.email.data
        toaddr = app.config["MY_EMAIL_ADDRESS"]
        msg['subject'] = form.subject.data
        msg['from'] = formataddr((str(Header(form.name.data, 'utf-8')), fromaddr))
        msg['to'] = toaddr
        msg['reply-to'] = fromaddr
        body = form.message.data
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(app.config['EMAIL_ACCOUNT'], app.config["EMAIL_PASSWORD"])
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return render_template('thanks.html')
    else:
        return render_template('contact.html', form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
