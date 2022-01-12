from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
import datetime as dt
import smtplib
from dotenv import load_dotenv
import os

app = Flask(__name__)
Bootstrap(app)
current_year = dt.datetime.now().year

# Environment Data
load_dotenv()
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ["PASSWORD"]
TO_EMAIL_ID = os.environ["TO_EMAIL_ID"]
app.config['SECRET_KEY'] = os.environ["VICKY_PY_SECRET_KEY"]


class ContactForm(FlaskForm):
    name = StringField(validators=[validators.DataRequired(message="Please Enter your name")])
    email = EmailField(label="Your Email",
                       validators=[validators.DataRequired(message="Please Enter your email ID."),
                                   validators.Email(message="Not a valid email Address")])
    message_subject = StringField(label="Subject",
                                  validators=[validators.DataRequired(message="Please Enter subject of message")])
    message = TextAreaField(label="Message", widget=TextArea())
    send_message = SubmitField(label="Send Message")


@app.route("/", methods=["POST", "GET"])
def home_page():
    contact_form = ContactForm()
    if request.method == "POST":
        name = contact_form.name.data
        email = contact_form.email.data
        mail_subject = contact_form.message_subject.data
        message = contact_form.message.data

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=TO_EMAIL_ID,
                                msg=f"Subject: {mail_subject}\nName:{name}\n\n{email}\n\n{message}")
        return redirect(url_for("home_page", msg="Successfully Sent the Message."))
    else:
        if request.args.get("msg"):
            msg = request.args.get("msg")
            return render_template("index.html", current_year=current_year, form=contact_form, msg=msg)
        else:
            return render_template("index.html", current_year=current_year, form=contact_form)


if __name__ == "__main__":
    app.run(debug=True)
