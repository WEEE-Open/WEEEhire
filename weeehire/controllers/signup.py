# -*- coding: utf-8 -*-
"""Signup controller module"""

import tg
import re
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
        email = twf.TextField(validator=PolitoMailVaildator)
    action = lurl('/signup/verify')
    submit = twf.SubmitButton(value='Submit')


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
            user = DBSession.query(User).filter_by(email_address=email).first()
            if not user:
                confirm_link = 'http://127.0.0.1:8080/signup/register?email='+email
                password = generate_password()
                confirm_link += '?passwd='+password
                mailer = get_mailer(request)
                message = Message(subject="Reclutamento WEEE Open",
                                  sender="no-reply@weeeopen.polito.it",
                                  recipients=[email],
                                  body="Ciao " + email[1:7] + " " + confirm_link)
                mailer.send(message)
            else:
                print('error_email_already_existing_in_db')
                return redirect("/signup")
            return redirect("/")
        else:
            return redirect("/signup")

    @expose('weeehire.templates.post_signup')
    def register(self, email, passwd, **kw):
        serial = email[1:7]
        print(serial)
        #u = User()
        #u.user_name = serial
        #u.display_name = serial
        #u.email_address = email
        #u.password = passwd

        #model.DBSession.add(u)
