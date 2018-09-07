# -*- coding: utf-8 -*-
"""Signup controller module"""

import re
from datetime import datetime
from tg import expose, redirect, validate, flash, lurl, request
# from tg.i18n import ugettext as _
# from tg import predicates

from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User
from tw2.core import RegexValidator, EmailValidator, Required, _
import tw2.forms as twf
from tgext.mailer import get_mailer, Message
import string
import secrets


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(16))
    return password


class PolitoMailVaildator(RegexValidator):
    msgs = {
        'badregex': ('bademail', _('Must be your polito mail address [sXXXXXX@studenti.polito.it]')),
    }
    regex = re.compile('^[\w\-.]+@studenti.polito.it+$')


class SignupForm(twf.Form):
    class child(twf.widgets.TableLayout):
        email = twf.TextField(validator=PolitoMailVaildator, css_class="form-control")
    action = lurl('/signup/verify')
    submit = twf.SubmitButton(value='Submit', css_class="btn btn-success")


class SignupController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    # allow_only = predicates.not_anonymous()
    
    @expose('weeehire.templates.signup')
    def index(self, **kw):
        return dict(page='signup-index', form=SignupForm)

    @expose()
    @validate(SignupForm, error_handler=index)
    def verify(self, **kw):
        email = kw['email']
        if email:
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
                                       "\nLa tua password: " + password + "   (se la perdi sono cazzi tuoi asd)" +
                                       "\nCiawa di nuovo")
                                  )
                mailer.send(message)
            else:
                print('error_user_already_existing_in_db')
                return redirect("/signup")
            return redirect("/")
        else:
            return redirect("/signup")

    @expose('weeehire.templates.post_signup')
    def register(self, email, auth, **kw):
        user = User.by_email_address(email)
        if user:
            if user.created:
                flash(_('User already verified'), 'warning')
                return dict()
            if user.token == auth:
                user.created = datetime.now()
            else:
                flash(_('Authentication failed'), 'error')
        else:
            flash(_('User not found'), 'error')
        DBSession.flush()
        return dict()
