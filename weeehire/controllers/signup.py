# -*- coding: utf-8 -*-
"""Signup controller module"""

from datetime import datetime
from tg import expose, redirect, validate, flash, lurl, request
from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User
from tw2.core import RegexValidator, EmailValidator, Required, _
import tw2.forms as twf
from tgext.mailer import get_mailer, Message
from string import ascii_letters, digits
from random import randint


def generate_password():
    alphabet = ascii_letters + digits
    password = ""
    for c in range(32):
        password += str(alphabet[randint(0, len(alphabet)-1)])
    return password


def is_polito_mail(email: str):
    if not email:
        return False
    if '@' not in email:
        return False
    if not email.split('@')[1]:
        return False
    if email.split('@')[1] != 'studenti.polito.it':
        return False
    if email.startswith('s') or email.startswith('S'):
        for i in range(1, 7):
            if not email[i].isdigit():
                return False
    else:
        return False
    return True


class SignupForm(twf.Form):
    class child(twf.widgets.BaseLayout):
        email = twf.TextField(css_class="form-control mt-10")
    action = lurl('/signup/verify')
    submit = twf.SubmitButton(value='Submit', css_class="btn btn-success mt-10")


class SignupController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    # allow_only = predicates.not_anonymous()
    
    @expose('weeehire.templates.signup')
    def index(self, status=None, **kw):
        if status == 'badmail':
            flash(_('Please, insert your polito email address [sXXXXXX@studenti.polito.it]'), 'error')
        if status == 'login':
            flash(_('This email is already registered, please login'), 'error')
        if status == 'success':
            flash(_('Check your email inbox and click on the activation link'))
        return dict(page='signup-index', form=SignupForm)

    @expose()
    def verify(self, **kw):
        email = kw['email']
        if is_polito_mail(email):
            user = User.by_email_address(email)
            if not user:
                confirm_link = 'http://127.0.0.1:8080/signup/register?email=' + email
                token = generate_password()
                confirm_link += '&auth=' + token
                password = generate_password()
                serial = email.split("@")[0]

                u = User()
                u.user_name = serial
                u.display_name = serial
                u.email_address = email
                u.token = token
                u.password = password
                DBSession.add(u)
                DBSession.flush()

                mailer = get_mailer(request)
                message = Message(subject="Reclutamento WEEE Open",
                                  sender="weeeopen@yandex.ru",
                                  recipients=[email],
                                  body=("Ciawa! asd\nClicca qua per attivare l'account " + confirm_link +
                                       "\nIl tuo username: " + serial +
                                       "\nLa tua password: " + password + "   (se la perdi sono cazzi tuoi asd)" +
                                       "\nCiawa di nuovo")
                                  )
                mailer.send(message)
            else:
                return redirect("/signup?status=login")
            return redirect("/signup?status=success")
        else:
            return redirect("/signup?status=badmail")

    @expose('weeehire.templates.post_signup')
    def register(self, email, auth, **kw):
        user = User.by_email_address(email)
        if user:
            if user.created:
                flash(_('User already verified'), 'warning')
                return dict()
            if user.token == auth:
                user.created = datetime.now()
                flash(_('Authentication successful'))
            else:
                flash(_('Authentication failed'), 'error')
        else:
            flash(_('User not found'), 'error')
        DBSession.flush()
        return dict()
